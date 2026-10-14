# A-REMOTE-011 Stage 3B: targeted TUNER helper correction

## Result

**PASS — PRIVATE CORRECTION AND BUILD VERIFICATION COMPLETE; HARDWARE EXECUTION NOT PERFORMED.**

The failed helper used `Preferences::begin("remote_pair", true)` to inspect pairing state. Arduino Preferences returns only a boolean from this call, so the helper could not distinguish an absent namespace on an unprovisioned device from a genuine NVS open error. The first authorized capsule attempt consequently returned `storage_error` before any write.

## Narrow correction

Only the private commissioning helper's state probe changed. It now uses the underlying ESP-IDF NVS read-only API:

- `nvs_open(..., NVS_READONLY, ...) == ESP_ERR_NVS_NOT_FOUND` means the namespace is absent and the state is empty;
- every other open error remains a fail-closed storage error;
- each key length is queried with `nvs_get_blob`;
- key-not-found is treated as absence for that key, while every other key-read error remains fail-closed;
- both absent keys mean empty, exactly one present key or an unexpected length means partial, and only 16-byte `pair_id` plus 32-byte `psk` means complete.

The existing production pairing reader, write sequence, recovery policy, RTCP implementation and unrelated NVS users were not changed. The retained capsule pair was not regenerated or modified.

## Verification

- Focused private capsule/storage-policy suite: **22/22 PASS**. Six added cases cover absent namespace, genuine open error, key-read error, one-key partial state, wrong-length partial state and exact complete state.
- Clean `esp32-a011-pairing` build: **PASS** using Espressif32 platform 7.0.1, Arduino framework 3.20017.241212, Xtensa toolchain 8.4.0 and esptool 4.11.0.
- Corrected firmware: 2,026,736 bytes (`0x1EECF0`), SHA-256 `b866918f5a63586c5ed28cb192d71a9b63c886b6d10cf0fdd4cc5a5e6198c7a7`.
- Static RAM: 86,032 of 327,680 bytes. Linked program use: 2,020,165 of 3,145,728 bytes; headroom 1,125,563 bytes.
- Both original private capsules remain 112 bytes and match their retained private manifest hashes. Their hashes and contents are intentionally not published.

## Scope and next gate

No device was accessed, no firmware was flashed, no capsule was transmitted, and no NVS, REMOTE or production source was modified. The previously installed failed helper remains the device state recorded by the prior Stage 3B report.

The next owner decision is whether to authorize application-only installation of this exact corrected TUNER helper, exact readback verification, and one transmission of the retained original TUNER capsule. Any REMOTE provisioning remains separately gated.
