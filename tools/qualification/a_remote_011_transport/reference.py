"""Executable RTCP/1 reference used only for public, non-secret test vectors."""

from __future__ import annotations

import hashlib
import hmac
import json
import struct
import sys
from dataclasses import dataclass

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


VERSION = 1
MAX_PLAINTEXT = 512
HANDSHAKE_HEADER = struct.Struct("!4sBBH")
RECORD_HEADER = struct.Struct("!4sBBH8sQHH")
CLIENT_HELLO = 1
SERVER_HELLO = 2
CLIENT_FINISH = 3
APPLICATION = 1


def hs_header(message_type: int, body_length: int) -> bytes:
    return HANDSHAKE_HEADER.pack(b"RTCP", VERSION, message_type, body_length)


def mac(key: bytes, label: bytes, *parts: bytes) -> bytes:
    return hmac.new(key, label + b"".join(parts), hashlib.sha256).digest()


def derive(psk: bytes, client_nonce: bytes, server_nonce: bytes, transcript: bytes):
    if len(psk) != 32 or len(client_nonce) != 16 or len(server_nonce) != 16:
        raise ValueError("invalid key or nonce length")
    transcript_hash = hashlib.sha256(transcript).digest()
    salt = hashlib.sha256(b"RTCP1 HKDF salt" + client_nonce + server_nonce).digest()

    def expand(label: bytes, length: int) -> bytes:
        return HKDF(
            algorithm=hashes.SHA256(), length=length, salt=salt,
            info=label + transcript_hash,
        ).derive(psk)

    return {
        "transcript_hash": transcript_hash,
        "c2s_key": expand(b"RTCP1 c2s key", 16),
        "s2c_key": expand(b"RTCP1 s2c key", 16),
        "c2s_nonce_prefix": expand(b"RTCP1 c2s nonce", 4),
        "s2c_nonce_prefix": expand(b"RTCP1 s2c nonce", 4),
        "session_id": expand(b"RTCP1 session id", 8),
    }


def make_handshake(psk: bytes, pairing_id: bytes, client_nonce: bytes, server_nonce: bytes):
    if len(pairing_id) != 16:
        raise ValueError("pairing_id must be 16 bytes")
    ch = hs_header(CLIENT_HELLO, 32) + pairing_id + client_nonce
    sh_prefix = hs_header(SERVER_HELLO, 48) + server_nonce
    server_proof = mac(psk, b"RTCP1 server proof", ch, sh_prefix)
    sh = sh_prefix + server_proof
    cf_prefix = hs_header(CLIENT_FINISH, 32)
    client_proof = mac(psk, b"RTCP1 client proof", ch, sh, cf_prefix)
    cf = cf_prefix + client_proof
    keys = derive(psk, client_nonce, server_nonce, ch + sh + cf)
    return ch, sh, cf, keys


@dataclass
class Direction:
    key: bytes
    nonce_prefix: bytes
    session_id: bytes
    next_counter: int = 1

    def seal(self, plaintext: bytes, record_type: int = APPLICATION) -> bytes:
        if len(plaintext) > MAX_PLAINTEXT:
            raise ValueError("plaintext too large")
        if self.next_counter < 1 or self.next_counter > 0xFFFFFFFFFFFFFFFF:
            raise ValueError("counter exhausted")
        counter = self.next_counter
        header = RECORD_HEADER.pack(
            b"RTCR", VERSION, record_type, 0, self.session_id,
            counter, len(plaintext), 0,
        )
        nonce = self.nonce_prefix + counter.to_bytes(8, "big")
        result = header + AESGCM(self.key).encrypt(nonce, plaintext, header)
        self.next_counter += 1
        return result

    def open(self, record: bytes) -> bytes:
        if len(record) < RECORD_HEADER.size + 16:
            raise ValueError("truncated record")
        magic, version, _rtype, flags, session, counter, length, reserved = (
            RECORD_HEADER.unpack(record[: RECORD_HEADER.size])
        )
        if magic != b"RTCR" or version != VERSION or flags != 0 or reserved != 0:
            raise ValueError("invalid header")
        if session != self.session_id or counter != self.next_counter:
            raise ValueError("invalid session or counter")
        if length > MAX_PLAINTEXT or len(record) != RECORD_HEADER.size + length + 16:
            raise ValueError("invalid length")
        header = record[: RECORD_HEADER.size]
        nonce = self.nonce_prefix + counter.to_bytes(8, "big")
        plaintext = AESGCM(self.key).decrypt(nonce, record[RECORD_HEADER.size :], header)
        self.next_counter += 1
        return plaintext


def vector() -> dict[str, str]:
    psk = bytes(range(0x00, 0x20))
    pairing_id = bytes(range(0x40, 0x50))
    client_nonce = bytes(range(0x20, 0x30))
    server_nonce = bytes(range(0x30, 0x40))
    ch, sh, cf, keys = make_handshake(psk, pairing_id, client_nonce, server_nonce)
    sender = Direction(keys["c2s_key"], keys["c2s_nonce_prefix"], keys["session_id"])
    plaintext = b'{"kind":"test","value":17}'
    record = sender.seal(plaintext)
    values = {
        "warning": "PUBLIC TEST VECTOR ONLY; NEVER USE THIS PSK FOR A DEVICE",
        "psk": psk,
        "pairing_id": pairing_id,
        "client_nonce": client_nonce,
        "server_nonce": server_nonce,
        "client_hello": ch,
        "server_hello": sh,
        "client_finish": cf,
        **keys,
        "record_1_plaintext": plaintext,
        "record_1_wire": record,
    }
    return {name: value.hex() if isinstance(value, bytes) else value for name, value in values.items()}


if __name__ == "__main__":
    if sys.argv[1:] != ["--vectors"]:
        raise SystemExit("usage: reference.py --vectors")
    print(json.dumps(vector(), indent=2, sort_keys=True))
