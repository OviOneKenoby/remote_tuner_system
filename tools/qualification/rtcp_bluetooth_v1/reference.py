"""Executable, non-secret RTCP/1 Bluetooth Extension v1 codec reference.

This module models application plaintext only.  It deliberately reuses the
already-qualified RTCP/1 authenticated record layer instead of implementing
cryptography.
"""

from __future__ import annotations

import json
import struct
import sys
from dataclasses import dataclass


MAX_PLAINTEXT = 512
AUTHENTICATED_OVERHEAD = 28 + 16

LEGACY_CAPABILITY_REQUEST = b"\x03"
LEGACY_CAPABILITY_RESPONSE = bytes.fromhex(
    "04ff0000000000000002000007d00164"
)

BTX_CAPABILITY_RESPONSE = 12
BTX_STATE_REQUEST = 13
BTX_STATE_RESPONSE = 14
BTX_COMMAND = 15
COMMAND_RESULT = 8

BTX_MAJOR = 1
BTX_MINOR = 0
BTX_REVISION = 1
BTX_MAX_AGE_MS = 2000
MAX_ARTIST = 96
MAX_TITLE = 127

CAP_STATE = 1 << 0
CAP_METADATA = 1 << 1
CAP_PLAY = 1 << 2
CAP_PAUSE = 1 << 3
CAP_PREVIOUS = 1 << 4
CAP_NEXT = 1 << 5
CAP_ALL = 0x3F

SOURCE_NONE = 0
SOURCE_RADIO = 1
SOURCE_BLUETOOTH = 2
SOURCE_OTHER = 3

CONNECTION_NOT_APPLICABLE = 0
CONNECTION_UNKNOWN = 1
CONNECTION_DISCONNECTED = 2
CONNECTION_CONNECTED = 3

PLAYBACK_UNKNOWN = 0
PLAYBACK_STOPPED = 1
PLAYBACK_PLAYING = 2
PLAYBACK_PAUSED = 3

STATE_ARTIST = 1 << 0
STATE_TITLE = 1 << 1
STATE_PLAY = 1 << 2
STATE_PAUSE = 1 << 3
STATE_PREVIOUS = 1 << 4
STATE_NEXT = 1 << 5
STATE_KNOWN_FLAGS = 0x3F

OP_PLAY = 1
OP_PAUSE = 2
OP_PREVIOUS = 3
OP_NEXT = 4


def _u64(value: int) -> bytes:
    if value < 1 or value > 0xFFFFFFFFFFFFFFFF:
        raise ValueError("required u64 must be nonzero")
    return value.to_bytes(8, "big")


def _valid_text(raw: bytes) -> str:
    if not raw:
        raise ValueError("text must be nonempty")
    value = raw.decode("utf-8", errors="strict")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in value):
        raise ValueError("control character in text")
    return value


def bounded_utf8(value: str, maximum: int) -> bytes:
    raw = value.encode("utf-8", errors="strict")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in value):
        raise ValueError("control character in text")
    if len(raw) <= maximum:
        return raw
    raw = raw[:maximum]
    while raw:
        try:
            raw.decode("utf-8", errors="strict")
            return raw
        except UnicodeDecodeError:
            raw = raw[:-1]
    return b""


@dataclass(frozen=True)
class ExtensionCapabilities:
    flags: int = CAP_ALL
    max_artist: int = MAX_ARTIST
    max_title: int = MAX_TITLE
    max_age_ms: int = BTX_MAX_AGE_MS
    revision: int = BTX_REVISION


def encode_capabilities(value: ExtensionCapabilities = ExtensionCapabilities()) -> bytes:
    if value.flags & ~CAP_ALL or not (value.flags & CAP_STATE):
        raise ValueError("invalid capability flags")
    metadata = bool(value.flags & CAP_METADATA)
    if metadata != bool(value.max_artist or value.max_title):
        raise ValueError("metadata bounds disagree with capability")
    if value.max_artist > MAX_ARTIST or value.max_title > MAX_TITLE:
        raise ValueError("metadata bound too large")
    if value.max_age_ms != BTX_MAX_AGE_MS or value.revision != BTX_REVISION:
        raise ValueError("unsupported capability policy")
    return struct.pack(
        "!BBBBBBHQ",
        BTX_CAPABILITY_RESPONSE,
        BTX_MAJOR,
        BTX_MINOR,
        value.flags,
        value.max_artist,
        value.max_title,
        value.max_age_ms,
        value.revision,
    )


def decode_capabilities(payload: bytes) -> ExtensionCapabilities:
    if len(payload) != 16:
        raise ValueError("capability response must be 16 bytes")
    kind, major, minor, flags, artist, title, age, revision = struct.unpack(
        "!BBBBBBHQ", payload
    )
    if kind != BTX_CAPABILITY_RESPONSE or major != BTX_MAJOR or minor != BTX_MINOR:
        raise ValueError("unsupported extension identity")
    value = ExtensionCapabilities(flags, artist, title, age, revision)
    if encode_capabilities(value) != payload:
        raise ValueError("non-canonical capability response")
    return value


@dataclass(frozen=True)
class BluetoothState:
    source: int
    connection: int
    playback: int
    sequence: int
    source_generation: int
    metadata_revision: int
    artist: str = ""
    title: str = ""
    play: bool = False
    pause: bool = False
    previous: bool = False
    next: bool = False


def encode_state(value: BluetoothState) -> bytes:
    if value.source not in range(4) or value.connection not in range(4):
        raise ValueError("invalid source or connection")
    if value.playback not in range(4):
        raise ValueError("invalid playback state")

    artist = bounded_utf8(value.artist, MAX_ARTIST) if value.artist else b""
    title = bounded_utf8(value.title, MAX_TITLE) if value.title else b""
    flags = ((STATE_ARTIST if artist else 0) | (STATE_TITLE if title else 0) |
             (STATE_PLAY if value.play else 0) | (STATE_PAUSE if value.pause else 0) |
             (STATE_PREVIOUS if value.previous else 0) |
             (STATE_NEXT if value.next else 0))

    if value.source != SOURCE_BLUETOOTH:
        if value.connection != CONNECTION_NOT_APPLICABLE or value.playback != PLAYBACK_UNKNOWN:
            raise ValueError("non-Bluetooth source carries Bluetooth state")
        if flags:
            raise ValueError("non-Bluetooth source carries Bluetooth fields")
    else:
        if value.connection == CONNECTION_NOT_APPLICABLE:
            raise ValueError("Bluetooth source lacks connection state")
        if value.connection != CONNECTION_CONNECTED:
            if value.playback != PLAYBACK_UNKNOWN or flags:
                raise ValueError("unconnected Bluetooth source carries stale state")
        else:
            if value.play and value.playback not in (PLAYBACK_STOPPED, PLAYBACK_PAUSED):
                raise ValueError("play availability contradicts playback state")
            if value.pause and value.playback != PLAYBACK_PLAYING:
                raise ValueError("pause availability contradicts playback state")

    header = bytes((BTX_STATE_RESPONSE, BTX_MAJOR, value.source, value.connection,
                    value.playback, flags, len(artist), len(title)))
    payload = (header + _u64(value.sequence) + _u64(value.source_generation) +
               _u64(value.metadata_revision) + artist + title)
    if len(payload) > 255:
        raise AssertionError("state response exceeds specified bound")
    return payload


def decode_state(payload: bytes) -> BluetoothState:
    if len(payload) < 32 or len(payload) > 255:
        raise ValueError("state response length out of range")
    kind, major, source, connection, playback, flags, artist_n, title_n = payload[:8]
    if kind != BTX_STATE_RESPONSE or major != BTX_MAJOR or flags & ~STATE_KNOWN_FLAGS:
        raise ValueError("invalid state header")
    if artist_n > MAX_ARTIST or title_n > MAX_TITLE or len(payload) != 32 + artist_n + title_n:
        raise ValueError("invalid metadata lengths")
    if bool(flags & STATE_ARTIST) != bool(artist_n) or bool(flags & STATE_TITLE) != bool(title_n):
        raise ValueError("metadata flags disagree with lengths")
    sequence = int.from_bytes(payload[8:16], "big")
    generation = int.from_bytes(payload[16:24], "big")
    revision = int.from_bytes(payload[24:32], "big")
    if not sequence or not generation or not revision:
        raise ValueError("zero sequence, generation or revision")
    artist_b = payload[32:32 + artist_n]
    title_b = payload[32 + artist_n:]
    artist = _valid_text(artist_b) if artist_b else ""
    title = _valid_text(title_b) if title_b else ""
    value = BluetoothState(
        source, connection, playback, sequence, generation, revision,
        artist, title,
        bool(flags & STATE_PLAY), bool(flags & STATE_PAUSE),
        bool(flags & STATE_PREVIOUS), bool(flags & STATE_NEXT),
    )
    if encode_state(value) != payload:
        raise ValueError("non-canonical state response")
    return value


def state_request() -> bytes:
    return bytes((BTX_STATE_REQUEST,))


@dataclass(frozen=True)
class BluetoothCommand:
    request_id: int
    operation: int
    expected_playback: int
    source_generation: int


def encode_command(value: BluetoothCommand) -> bytes:
    if value.operation not in (OP_PLAY, OP_PAUSE, OP_PREVIOUS, OP_NEXT):
        raise ValueError("invalid operation")
    if value.expected_playback not in range(4):
        raise ValueError("invalid expected playback state")
    return (bytes((BTX_COMMAND,)) + _u64(value.request_id) +
            bytes((value.operation, value.expected_playback)) +
            _u64(value.source_generation))


def decode_command(payload: bytes) -> BluetoothCommand:
    if len(payload) != 19 or payload[0] != BTX_COMMAND:
        raise ValueError("command must be 19 bytes")
    value = BluetoothCommand(
        int.from_bytes(payload[1:9], "big"), payload[9], payload[10],
        int.from_bytes(payload[11:19], "big"),
    )
    if encode_command(value) != payload:
        raise ValueError("invalid command")
    return value


def encode_result(request_id: int, accepted: bool, error: int) -> bytes:
    if accepted != (error == 0) or error not in range(8):
        raise ValueError("invalid result")
    return bytes((COMMAND_RESULT,)) + _u64(request_id) + bytes((int(accepted), error))


@dataclass(frozen=True)
class CommandResult:
    request_id: int
    accepted: bool
    error: int


def decode_result(payload: bytes) -> CommandResult:
    if len(payload) != 11 or payload[0] != COMMAND_RESULT:
        raise ValueError("result must be 11 bytes")
    value = CommandResult(
        int.from_bytes(payload[1:9], "big"), bool(payload[9]), payload[10]
    )
    if payload[9] not in (0, 1) or encode_result(
        value.request_id, value.accepted, value.error
    ) != payload:
        raise ValueError("invalid result")
    return value


class ExtensionProbe:
    """Session-scoped model of the selected two-query negotiation."""

    def __init__(self, extension_aware: bool):
        self.extension_aware = extension_aware
        self.first_capability_seen = False
        self.probe_window = False
        self.negotiated = False
        self.legacy_locked = False

    def reset(self) -> None:
        self.__init__(self.extension_aware)

    def request(self, payload: bytes) -> bytes:
        if payload == LEGACY_CAPABILITY_REQUEST and not self.first_capability_seen:
            self.first_capability_seen = True
            self.probe_window = True
            return LEGACY_CAPABILITY_RESPONSE
        if payload == LEGACY_CAPABILITY_REQUEST and self.probe_window:
            self.probe_window = False
            if self.extension_aware:
                self.negotiated = True
                return encode_capabilities()
            self.legacy_locked = True
            return LEGACY_CAPABILITY_RESPONSE
        if self.probe_window:
            self.probe_window = False
            self.legacy_locked = True
        raise ValueError("request outside the reference negotiation model")


def vectors() -> dict[str, object]:
    state = BluetoothState(
        SOURCE_BLUETOOTH, CONNECTION_CONNECTED, PLAYBACK_PLAYING,
        7, 3, 5, "Example Artist", "Example Title",
        pause=True, previous=True, next=True,
    )
    maximum = BluetoothState(
        SOURCE_BLUETOOTH, CONNECTION_CONNECTED, PLAYBACK_PAUSED,
        8, 3, 6, "A" * MAX_ARTIST, "T" * MAX_TITLE,
        play=True, previous=True, next=True,
    )
    command = BluetoothCommand(0x0102030405060708, OP_PAUSE, PLAYBACK_PLAYING, 3)
    encoded_maximum = encode_state(maximum)
    return {
        "warning": "PUBLIC NON-SECRET APPLICATION CODEC VECTORS; NO OPERATIONAL DATA",
        "legacy_capability_request": LEGACY_CAPABILITY_REQUEST.hex(),
        "legacy_capability_response": LEGACY_CAPABILITY_RESPONSE.hex(),
        "extension_capability_response": encode_capabilities().hex(),
        "state_request": state_request().hex(),
        "bluetooth_state_response": encode_state(state).hex(),
        "bluetooth_state_maximum": encoded_maximum.hex(),
        "bluetooth_state_maximum_plaintext_bytes": len(encoded_maximum),
        "bluetooth_state_maximum_authenticated_bytes": len(encoded_maximum) + AUTHENTICATED_OVERHEAD,
        "bluetooth_command": encode_command(command).hex(),
        "accepted_command_result": encode_result(command.request_id, True, 0).hex(),
        "stale_command_result": encode_result(command.request_id, False, 4).hex(),
    }


if __name__ == "__main__":
    if sys.argv[1:] != ["--vectors"]:
        raise SystemExit("usage: reference.py --vectors")
    print(json.dumps(vectors(), indent=2, sort_keys=True))
