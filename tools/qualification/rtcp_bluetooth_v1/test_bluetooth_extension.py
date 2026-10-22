import json
import unittest
from pathlib import Path

from reference import (
    AUTHENTICATED_OVERHEAD,
    BTX_CAPABILITY_RESPONSE,
    BTX_MAX_AGE_MS,
    CAP_ALL,
    CONNECTION_CONNECTED,
    CONNECTION_DISCONNECTED,
    CONNECTION_NOT_APPLICABLE,
    ExtensionProbe,
    LEGACY_CAPABILITY_REQUEST,
    LEGACY_CAPABILITY_RESPONSE,
    MAX_ARTIST,
    MAX_PLAINTEXT,
    MAX_TITLE,
    OP_NEXT,
    OP_PAUSE,
    PLAYBACK_PLAYING,
    PLAYBACK_UNKNOWN,
    SOURCE_BLUETOOTH,
    SOURCE_RADIO,
    BluetoothCommand,
    BluetoothState,
    bounded_utf8,
    decode_capabilities,
    decode_command,
    decode_result,
    decode_state,
    encode_capabilities,
    encode_command,
    encode_result,
    encode_state,
    state_request,
    vectors,
)


class BluetoothExtensionTests(unittest.TestCase):
    def test_committed_vectors_are_deterministic(self):
        committed = json.loads(
            Path(__file__).with_name("test_vectors.json").read_text(encoding="utf-8")
        )
        self.assertEqual(vectors(), committed)

    def test_old_remote_new_tuner_receives_exact_legacy_first_response(self):
        server = ExtensionProbe(extension_aware=True)
        self.assertEqual(server.request(LEGACY_CAPABILITY_REQUEST), LEGACY_CAPABILITY_RESPONSE)
        self.assertFalse(server.negotiated)

    def test_new_remote_old_tuner_falls_back_without_disconnect(self):
        server = ExtensionProbe(extension_aware=False)
        self.assertEqual(server.request(LEGACY_CAPABILITY_REQUEST), LEGACY_CAPABILITY_RESPONSE)
        self.assertEqual(server.request(LEGACY_CAPABILITY_REQUEST), LEGACY_CAPABILITY_RESPONSE)
        self.assertTrue(server.legacy_locked)

    def test_new_remote_new_tuner_negotiates_only_on_second_query(self):
        server = ExtensionProbe(extension_aware=True)
        server.request(LEGACY_CAPABILITY_REQUEST)
        response = server.request(LEGACY_CAPABILITY_REQUEST)
        self.assertEqual(response[0], BTX_CAPABILITY_RESPONSE)
        self.assertEqual(decode_capabilities(response).flags, CAP_ALL)
        self.assertTrue(server.negotiated)

    def test_any_intervening_legacy_request_closes_probe_window(self):
        server = ExtensionProbe(extension_aware=True)
        server.request(LEGACY_CAPABILITY_REQUEST)
        with self.assertRaises(ValueError):
            server.request(b"\x05")
        self.assertTrue(server.legacy_locked)
        self.assertFalse(server.negotiated)

    def test_negotiation_is_session_scoped(self):
        server = ExtensionProbe(extension_aware=True)
        server.request(LEGACY_CAPABILITY_REQUEST)
        server.request(LEGACY_CAPABILITY_REQUEST)
        server.reset()
        self.assertFalse(server.negotiated)
        self.assertEqual(server.request(LEGACY_CAPABILITY_REQUEST), LEGACY_CAPABILITY_RESPONSE)

    def test_capability_policy_and_bounds(self):
        decoded = decode_capabilities(encode_capabilities())
        self.assertEqual(decoded.max_artist, MAX_ARTIST)
        self.assertEqual(decoded.max_title, MAX_TITLE)
        self.assertEqual(decoded.max_age_ms, BTX_MAX_AGE_MS)

    def test_bluetooth_metadata_and_playback_round_trip(self):
        value = BluetoothState(
            SOURCE_BLUETOOTH, CONNECTION_CONNECTED, PLAYBACK_PLAYING,
            1, 2, 3, "Artist", "Title", pause=True, previous=True, next=True,
        )
        self.assertEqual(decode_state(encode_state(value)), value)

    def test_non_bluetooth_response_clears_all_bluetooth_state(self):
        value = BluetoothState(
            SOURCE_RADIO, CONNECTION_NOT_APPLICABLE, PLAYBACK_UNKNOWN, 2, 3, 4
        )
        self.assertEqual(decode_state(encode_state(value)), value)

    def test_disconnected_phone_cannot_retain_metadata_or_commands(self):
        with self.assertRaises(ValueError):
            encode_state(BluetoothState(
                SOURCE_BLUETOOTH, CONNECTION_DISCONNECTED, PLAYBACK_UNKNOWN,
                1, 2, 3, "stale", "stale", next=True,
            ))

    def test_command_round_trip(self):
        command = BluetoothCommand(9, OP_PAUSE, PLAYBACK_PLAYING, 4)
        self.assertEqual(decode_command(encode_command(command)), command)

    def test_command_result_correlation_layout(self):
        accepted = encode_result(9, True, 0)
        stale = encode_result(9, False, 4)
        self.assertEqual(len(accepted), 11)
        self.assertTrue(decode_result(accepted).accepted)
        self.assertEqual(decode_result(stale).error, 4)
        with self.assertRaises(ValueError):
            encode_result(9, True, 4)
        with self.assertRaises(ValueError):
            decode_result(bytes((8,)) + bytes(10))

    def test_maximum_payload_and_authenticated_record_fit(self):
        payload = encode_state(BluetoothState(
            SOURCE_BLUETOOTH, CONNECTION_CONNECTED, 3, 1, 2, 3,
            "A" * MAX_ARTIST, "T" * MAX_TITLE,
            play=True, previous=True, next=True,
        ))
        self.assertEqual(len(payload), 255)
        self.assertEqual(len(payload) + AUTHENTICATED_OVERHEAD, 299)
        self.assertLessEqual(len(payload), MAX_PLAINTEXT)

    def test_utf8_truncation_never_splits_codepoint(self):
        result = bounded_utf8("é" * 100, MAX_ARTIST)
        self.assertEqual(len(result), MAX_ARTIST)
        self.assertEqual(result.decode("utf-8"), "é" * 48)

    def test_malformed_utf8_rejected(self):
        payload = bytearray(encode_state(BluetoothState(
            SOURCE_BLUETOOTH, CONNECTION_CONNECTED, PLAYBACK_UNKNOWN,
            1, 2, 3, artist="A",
        )))
        payload[32] = 0xFF
        with self.assertRaises(UnicodeDecodeError):
            decode_state(bytes(payload))

    def test_invalid_lengths_enums_and_reserved_bits_rejected(self):
        with self.assertRaises(ValueError):
            decode_state(bytes(31))
        good = bytearray(encode_state(BluetoothState(
            SOURCE_BLUETOOTH, CONNECTION_CONNECTED, PLAYBACK_UNKNOWN,
            1, 2, 3,
        )))
        good[2] = 4
        with self.assertRaises(ValueError):
            decode_state(bytes(good))
        good[2] = SOURCE_BLUETOOTH
        good[5] = 0x80
        with self.assertRaises(ValueError):
            decode_state(bytes(good))
        with self.assertRaises(ValueError):
            decode_command(bytes((15,)) + bytes(18))

    def test_state_request_is_one_byte_and_command_is_nineteen(self):
        self.assertEqual(state_request(), b"\x0d")
        self.assertEqual(
            len(encode_command(BluetoothCommand(1, OP_NEXT, PLAYBACK_UNKNOWN, 1))),
            19,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
