# A-REMOTE-010 Stage 4 completion

Recorded UTC: 2026-10-13T14:30:38Z. Stage input `ee6a29bffe0bea5bc6eca8df1975a7390d612c5e`; [owner authorization and reset confirmation](../references/A010_STAGE4_FINAL_RECOVER_OWNER_AUTHORIZATION_2026-10-13.md); [protocol](../protocols/A-REMOTE-010_HARDWARE_VALIDATION.md); [sanitized result](../references/device_evidence/remote/A-REMOTE-010/STAGE4_RESULT.json).

**PASS — CONTROLLED INITIALIZATION SURVIVED A NORMAL REBOOT; STAGE 4 COMPLETE; STOPPED BEFORE STAGE 5.**

The prior Stage 4 evidence remains preserved: the exact confirmed `INIT` ran once, transitioned erased generation 0/next 0 to initialized-empty generation 0/next 1, and immediate `STATUS` passed. The subsequent automated reset attempts did not establish a normal boot and were recorded as stopped partial results.

For this final continuation, the owner performed a normal hardware reset out of ROM download mode and confirmed that REMOTE's UI was functional. No executor reset was performed. COM3 was re-established without toggling reset lines, and exactly one `!A010 RECOVER` was transmitted.

The installed A010 diagnostic firmware returned exactly one accepted response. It reported the exact data/NVS partition at `0x00E20000`, size `0x10000`, schema 1, `state=initialized_empty`, generation 0, next generation 1, no incomplete transaction, 10 used, 2,006 free and 1,880 available entries, with `payload_logged=0` and no unexpected error. The exact diagnostic response verifies the running A010 candidate and demonstrates that initialization survived the owner-confirmed normal reboot.

The owner-confirmed functional UI supports retained existing observable configuration; no setting was changed in this continuation. No `INIT`, `STATUS`, `COMMIT1`, `COMMIT2`, `ERASE` or other command was sent. No firmware was flashed, no source code changed and no additional reset was performed.

The private 250-byte UART capture has SHA-256 `79e80674da21c216f99a13854aa2cb6a37c48a21edde74ca07dfd546f5f7c521` and is not published. Stage 5 remains unexecuted and requires separate explicit owner authorization.
