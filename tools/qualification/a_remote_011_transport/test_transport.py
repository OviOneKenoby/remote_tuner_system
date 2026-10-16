import json
import unittest
from pathlib import Path

from cryptography.exceptions import InvalidTag

from reference import Direction, MAX_PLAINTEXT, make_handshake, vector


PSK = bytes(range(0x00, 0x20))
PAIRING = bytes(range(0x40, 0x50))
CN = bytes(range(0x20, 0x30))
SN = bytes(range(0x30, 0x40))


def session(cn=CN, sn=SN):
    return make_handshake(PSK, PAIRING, cn, sn)


class TransportTests(unittest.TestCase):
    def directions(self):
        _, _, _, keys = session()
        tx = Direction(keys["c2s_key"], keys["c2s_nonce_prefix"], keys["session_id"])
        rx = Direction(keys["c2s_key"], keys["c2s_nonce_prefix"], keys["session_id"])
        return tx, rx

    def test_public_vector_is_deterministic(self):
        committed = json.loads(Path(__file__).with_name("test_vectors.json").read_text(encoding="utf-8-sig"))
        self.assertEqual(vector(), committed)

    def test_mutual_proofs_change_with_psk(self):
        ch, sh, cf, _ = session()
        _, wrong_sh, wrong_cf, _ = make_handshake(bytes(reversed(PSK)), PAIRING, CN, SN)
        self.assertEqual(ch, session()[0])
        self.assertNotEqual(sh, wrong_sh)
        self.assertNotEqual(cf, wrong_cf)

    def test_directional_keys_and_nonces_are_distinct(self):
        *_, keys = session()
        self.assertNotEqual(keys["c2s_key"], keys["s2c_key"])
        self.assertNotEqual(keys["c2s_nonce_prefix"], keys["s2c_nonce_prefix"])

    def test_round_trip(self):
        tx, rx = self.directions()
        self.assertEqual(rx.open(tx.seal(b"volume.set")), b"volume.set")

    def test_512_bytes_allowed(self):
        tx, rx = self.directions()
        payload = bytes(range(256)) * 2
        self.assertEqual(rx.open(tx.seal(payload)), payload)

    def test_513_bytes_rejected(self):
        tx, _ = self.directions()
        with self.assertRaises(ValueError):
            tx.seal(bytes(MAX_PLAINTEXT + 1))

    def test_duplicate_counter_rejected(self):
        tx, rx = self.directions()
        record = tx.seal(b"once")
        self.assertEqual(rx.open(record), b"once")
        with self.assertRaises(ValueError):
            rx.open(record)

    def test_gap_counter_rejected(self):
        tx, rx = self.directions()
        tx.seal(b"counter one")
        with self.assertRaises(ValueError):
            rx.open(tx.seal(b"counter two"))

    def test_header_tamper_rejected(self):
        tx, rx = self.directions()
        record = bytearray(tx.seal(b"header"))
        record[7] ^= 1
        with self.assertRaises(ValueError):
            rx.open(bytes(record))

    def test_ciphertext_tamper_rejected(self):
        tx, rx = self.directions()
        record = bytearray(tx.seal(b"ciphertext"))
        record[-17] ^= 1
        with self.assertRaises(InvalidTag):
            rx.open(bytes(record))

    def test_tag_tamper_rejected(self):
        tx, rx = self.directions()
        record = bytearray(tx.seal(b"tag"))
        record[-1] ^= 1
        with self.assertRaises(InvalidTag):
            rx.open(bytes(record))

    def test_old_session_record_rejected_after_reconnect(self):
        tx, _ = self.directions()
        old_record = tx.seal(b"old")
        _, _, _, keys = session(bytes(range(0x21, 0x31)), bytes(range(0x31, 0x41)))
        new_rx = Direction(keys["c2s_key"], keys["c2s_nonce_prefix"], keys["session_id"])
        with self.assertRaises(ValueError):
            new_rx.open(old_record)

    def test_counter_exhaustion_rejected(self):
        tx, _ = self.directions()
        tx.next_counter = 0x10000000000000000
        with self.assertRaises(ValueError):
            tx.seal(b"never")

    def test_truncation_rejected(self):
        tx, rx = self.directions()
        record = tx.seal(b"complete")
        with self.assertRaises(ValueError):
            rx.open(record[:-1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
