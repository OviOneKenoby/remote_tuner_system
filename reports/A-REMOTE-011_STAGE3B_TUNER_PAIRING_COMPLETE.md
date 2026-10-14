# A-REMOTE-011 Stage 3B: corrected TUNER pairing execution

## Result

**PASS — TUNER PAIRING PROVISIONED BY ONE AUTHORIZED CAPSULE TRANSMISSION.**

The corrected private commissioning helper and retained original TUNER capsule were used under the owner-authorized one-shot procedure. REMOTE was disconnected and was not accessed or provisioned.

## Preconditions

- Coordination head matched approved correction commit `2394574b84eb3cbe5a92d3130b44683ec2f1de18` locally and on the remote branch.
- Every manifest-listed Stage 1 TUNER rollback file was present and matched its recorded byte length and SHA-256.
- The retained TUNER capsule remained 112 bytes and matched its private manifest. Neither capsule, pairing identifier nor PSK was regenerated or changed.
- The connected interface was positively identified through the ROM as the accepted classic ESP32 TUNER with 4 MiB physical flash. Device-specific identifiers remain private.
- Corrected firmware identity matched: 2,026,736 bytes (`0x1EECF0`), SHA-256 `b866918f5a63586c5ed28cb192d71a9b63c886b6d10cf0fdd4cc5a5e6198c7a7`.

## Application-only installation

One esptool write at 921600 baud installed only the corrected application at `0x10000`, preserving flash mode, frequency and size. Esptool erased the covering application sectors `0x10000–0x1FEFFF`, wrote the image through `0x1FECEF` (exclusive end `0x1FECF0`), and reported successful write-time hash verification. No separate erase and no bootloader, partition-table, OTA-metadata or NVS image write was issued.

An independent readback of exactly 2,026,736 bytes from `0x10000` matched the approved candidate SHA-256.

## One-shot provisioning

The corrected commissioning identity and normal setup completion were confirmed before transmission. The retained original TUNER capsule was transmitted exactly once. The sanitized response was:

`A011_PAIR result=complete secret_output=0`

No retry followed. The complete private UART capture was retained and hashed before parsing; neither its contents nor any secret-derived capsule data is published.

## Scope and next gate

TUNER pairing storage is now provisioned. The corrected helper remains installed. Production firmware was not restored, REMOTE was not accessed or provisioned, no RTCP command was issued, and PR #17 remains open and unmerged.

The next owner decision is whether to authorize the separately gated REMOTE commissioning-helper installation and exactly one transmission of the retained original REMOTE capsule. TUNER production-firmware restoration remains deferred until directed by the staged procedure.
