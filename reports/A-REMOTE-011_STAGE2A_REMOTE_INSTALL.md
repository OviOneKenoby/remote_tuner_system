# A-REMOTE-011 Stage 2A: REMOTE application installation

## Result

**PASS — REMOTE PHASE 3 APPLICATION INSTALLED AND VERIFIED; TUNER UNTOUCHED.**

The owner-authorized REMOTE-only Stage 2A operation used the Phase 3 candidate identified below. The device was positively identified through its ESP32-S3 ROM interface and retained the expected 16 MiB physical flash identity before the single write.

## Pre-write checks

- Candidate: 2,515,584 bytes (`0x266280`), SHA-256 `ceae9f64329c5409fdfe92e5ac5394885010abf1cf66ac24a5ab7fcc35f11647`.
- Candidate identity matched the accepted Phase 3 evidence exactly.
- Verified Stage 1 rollback span remained available: 2,515,584 bytes, SHA-256 `0f89125f8dd7833920c3bb35aa83961286ac21cf13fceec59f20c456f6cf2ffa`.
- The Stage 1 full-flash and rollback-critical backups had already been preserved on separate physical USB storage; originals remained intact.

## Write and independent verification

Exactly one esptool application write was issued at offset `0x10000`, with flash mode, frequency and size set to `keep`. The only image argument was the authorized candidate. Esptool necessarily erased the covering application sectors `0x10000–0x276FFF`, wrote the `0x266280` candidate bytes through `0x27627F`, and reported successful write-time data-hash verification. No retry or rollback occurred.

An independent readback covered exactly `0x10000–0x27627F`:

- readback size: 2,515,584 bytes;
- readback SHA-256: `ceae9f64329c5409fdfe92e5ac5394885010abf1cf66ac24a5ab7fcc35f11647`;
- candidate/readback equality: PASS.

The dedicated `remote_ctl` partition was read after installation and remained byte-identical to the Stage 1 baseline: 65,536 bytes, SHA-256 `6bb3aa0c903d59ee1b341a828b61424be73327b270bd0fd662a4c2cb891db1e0`. Its contents were not decoded or published.

## Boot and functional verification

The normal boot log confirmed:

- the unchanged seven-entry partition table;
- selection and loading of the factory application at `0x10000`;
- no observed partition error, panic, watchdog reset, Guru Meditation, or boot loop;
- Wi-Fi association succeeded without changing stored configuration;
- the A-011 client reported `configured=0` and `unconfigured_write=0`, confirming that the unpaired client remained disabled and performed no provisioning write.

The owner then confirmed, without changing settings:

- normal REMOTE UI: PASS;
- previously stored configuration: PASS;
- one ordinary sleep/wake cycle: PASS.

## Scope and next gate

The bootloader, partition table, default NVS, OTA metadata and `remote_ctl` were not written. No PSK was generated, pairing was not provisioned, no RTCP command was issued, and TUNER was not accessed or modified.

Stage 2A is complete at the approved practical hobby/public-beta level. Stage 2B TUNER installation remains unauthorized and requires a separate owner decision. PR #17 remains open and unmerged.
