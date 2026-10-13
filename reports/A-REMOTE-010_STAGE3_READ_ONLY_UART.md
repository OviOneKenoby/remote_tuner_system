# A-REMOTE-010 Stage 3 read-only UART validation

Recorded UTC: 2026-10-13T07:28:53Z. Stage input `06439250ffb8fe2ff9502823461228afa32c6537`; [owner authorization](../references/A010_STAGE3_READ_ONLY_UART_OWNER_AUTHORIZATION_2026-10-13.md); [protocol](../protocols/A-REMOTE-010_HARDWARE_VALIDATION.md); [sanitized result](../references/device_evidence/remote/A-REMOTE-010/STAGE3_RESULT.json).

**PASS — READ-ONLY UART DIAGNOSTIC VALIDATION COMPLETE. `remote_ctl` IS READY FOR SEPARATELY AUTHORIZED INITIALIZATION.**

The established COM3 USB-serial connection was opened at 115200 baud without a reset. Exactly `!A010 INFO` and `!A010 STATUS` were sent once each. Each command produced exactly one `A010_PERSIST_DIAG` response and was accepted.

Both responses independently reported the required identity and state: partition exists, type 1/data, subtype 2/NVS, offset `0x00E20000`, size `0x10000`, `state=erased`, schema 1, generation 0, next generation 0 and no incomplete transaction. Entry counts were zero because the erased-state inspection returns before opening NVS. Both responses explicitly reported `payload_logged=0`.

No wrong-partition, corrupt, ambiguous, schema-mismatch, storage-error or other unexpected diagnostic result appeared. The 460-byte raw UART capture is retained privately with SHA-256 `733707773f0ead4d659f26b8a2a5feca0f377095baa33eced6e75a9fdfb272ab`; it is not published. Sanitized evidence contains only structural fields and counts.

No firmware was flashed and no source code changed. No `INIT`, `COMMIT1`, `COMMIT2`, `ERASE`, `RECOVER` or other command was sent. Stage 4 remains unexecuted and requires explicit owner authorization. The narrow Stage 3 result supports readiness to initialize the exact erased `remote_ctl` partition; it does not itself initialize or mutate it.
