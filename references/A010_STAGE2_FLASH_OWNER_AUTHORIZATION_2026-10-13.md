# A-REMOTE-010 Stage 2 diagnostic firmware authorization

Recorded 2026-10-13. The owner authorized Stage 2 of the published hardware-validation protocol using the validated diagnostic firmware with SHA-256 `308181d4144494734fe8fae360938f74b9f886fb4c41bff0cba9b89427e4d248` and verified COM3.

The authorization permitted flashing only that firmware at `0x10000`, followed by exact readback, normal-boot and diagnostic-identity verification, owner observation of existing UI/configuration, and a read-only check that `remote_ctl` remained unchanged. Bootloader, partition table, default NVS, OTA metadata and `remote_ctl` writes were prohibited. `INIT`, `COMMIT1`, `COMMIT2` and `ERASE` were prohibited. Execution had to stop after Stage 2.
