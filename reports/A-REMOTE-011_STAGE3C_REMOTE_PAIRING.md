# A-REMOTE-011 Stage 3C: REMOTE pairing

## Result

**PASS — REMOTE PAIRING PROVISIONED BY ONE AUTHORIZED CAPSULE TRANSMISSION.**

The accepted private REMOTE commissioning helper and retained original REMOTE capsule were used under the owner-authorized one-shot procedure. TUNER was not accessed or modified.

## Preconditions

- The retained Stage 1 REMOTE rollback set was present and every manifest-listed file matched its recorded byte length and SHA-256.
- The retained REMOTE capsule remained 112 bytes and matched its private manifest. Neither capsule, pairing identifier nor PSK was regenerated or changed.
- The connected interface was positively identified through the ROM as the accepted ESP32-S3 REMOTE with 16 MiB physical flash. Device-specific identifiers remain private.
- Helper identity matched: 2,517,248 bytes, SHA-256 `acb1948f791557e4a82adfde5228871e8a5e3602b937fff407426966031696a2`.

## Application-only installation

One esptool write at 921600 baud installed only the helper application at `0x10000`, preserving flash mode, frequency and size. Esptool erased only the covering application sectors and reported successful write-time hash verification. No separate erase and no bootloader, partition-table, OTA-metadata, default-NVS or `remote_ctl` image write was issued.

An independent readback of exactly 2,517,248 bytes from `0x10000` matched the approved helper SHA-256.

## Pre-provision state and one-shot result

Because this commissioning build intentionally excludes the A-010 diagnostic command set, state confirmation used a read-only physical comparison. The complete 65,536-byte `remote_ctl` partition was read immediately before provisioning and was byte-identical to the accepted Stage 1 capture. That accepted capture records the healthy recoverable generation-2 state, with no incomplete transaction, preserved through the later REMOTE installation evidence.

The helper additionally enforced the capsule's expected active generation 2 and fail-closed storage checks before committing. The retained original REMOTE capsule was transmitted exactly once. The sanitized response was:

`A011_PAIR result=complete secret_output=0`

This result is emitted only after the association commit and independent read-only recovery verification succeed. The commit used the backend's next generation, preserving the existing generation history. No retry followed. The private UART capture was retained and hashed before parsing; its contents and secret-derived data remain unpublished.

## Scope and next gate

Both TUNER and REMOTE pairing stores are now provisioned with the same retained private association. The REMOTE commissioning helper remains installed. TUNER was not modified, production firmware was not restored on either device, no RTCP command was issued, and PR #17 remains open and unmerged.

The next owner decision is whether to authorize the staged production-firmware restoration and subsequent read-only authenticated identity/capability/state verification. Any control mutation remains separately gated.
