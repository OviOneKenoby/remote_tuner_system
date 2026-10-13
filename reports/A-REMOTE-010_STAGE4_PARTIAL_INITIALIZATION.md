# A-REMOTE-010 Stage 4 controlled initialization partial result

Recorded UTC: 2026-10-13T07:37:58Z. Stage input `3094918af6b50f2fcfe48c1d749435973cb23fa3`; [owner authorization](../references/A010_STAGE4_INIT_OWNER_AUTHORIZATION_2026-10-13.md); [protocol](../protocols/A-REMOTE-010_HARDWARE_VALIDATION.md); [sanitized result](../references/device_evidence/remote/A-REMOTE-010/STAGE4_PARTIAL_RESULT.json).

**STOPPED / INCOMPLETE — INITIALIZATION AND IMMEDIATE STATUS PASSED; REBOOT WAS NOT VERIFIED; RECOVER WAS NOT SENT.** This is not a Stage 4 PASS.

The exact initialization command was transmitted once. It produced exactly one accepted response and the required transition: erased generation 0/next 0/no incomplete transaction to initialized-empty generation 0/next 1/no incomplete transaction. It reported 10 used, 2,006 free and 1,880 available entries and `payload_logged=0`. Initialization must not be repeated.

The immediately following `!A010 STATUS` was sent once and accepted. It independently confirmed the exact data/NVS partition at `0x00E20000`, size `0x10000`, schema 1, initialized-empty state, generation 0, next 1, no incomplete transaction, the same entry counts and no payload logging.

The runner then issued one serial reset signal and observed the port for 20 seconds. It received neither an ESP32-S3 ROM boot banner nor the A010 diagnostic identity. No panic or watchdog text was observed, but absence of those strings does not prove a reboot occurred. The protocol's unexpected-result STOP applied. `!A010 RECOVER` was not sent, no reset or initialization was retried, and post-reboot UI/configuration were not assessed.

No `COMMIT1`, `COMMIT2`, `ERASE` or other command was sent. No firmware was flashed and no source code changed. The last directly verified persistent state is initialized-empty generation 0/next 1 before the unverified reset signal. Reboot survival remains NOT VERIFIED.

The private 1,666-byte capture has SHA-256 `3286e6a7e4a1e512dfaa8703c34b4ea9cb9e279fba8170e384ad03ade40f2455` and is not published. A new owner decision is required for a narrowly scoped reset/reboot-verification and read-only `RECOVER` continuation. It must explicitly prohibit repeating `INIT`.
