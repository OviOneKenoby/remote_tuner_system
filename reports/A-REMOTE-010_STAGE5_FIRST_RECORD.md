# A-REMOTE-010 Stage 5 first-record validation

Recorded UTC: 2026-10-13T14:40:01Z. Stage input `dd746b698c92962c5c8158a9cf5886dba3df177b`; [owner authorization](../references/A010_STAGE5_COMMIT1_OWNER_AUTHORIZATION_2026-10-13.md); [protocol](../protocols/A-REMOTE-010_HARDWARE_VALIDATION.md); [sanitized result](../references/device_evidence/remote/A-REMOTE-010/STAGE5_RESULT.json).

**PASS — FIRST TEST RECORD COMMITTED AND RECOVERED AFTER NORMAL REBOOT; STOPPED BEFORE STAGE 6.**

The exact confirmed `COMMIT1` command was transmitted once. It produced one accepted response and the required transition: initialized-empty generation 0/next 1/no incomplete transaction to valid-recoverable generation 1/next 2/no incomplete transaction. It reported 14 used, 2,002 free and 1,876 available entries, `payload_logged=0` and no unexpected error.

The owner then performed the same proven normal physical reset used to complete Stage 4. The prohibited USB-JTAG ROM reset sequence was not used. After COM3 returned, exactly one read-only `!A010 RECOVER` was transmitted. It produced one accepted response with the exact data/NVS partition identity at `0x00E20000`, size `0x10000`, schema 1, valid-recoverable generation 1, next 2, no incomplete transaction, the same entry counts, no payload logging and no unexpected error. The first test record therefore survived the normal reboot.

The owner confirmed that the UI was functional and the existing observable configuration remained present. No setting was changed. `INIT` and `COMMIT1` were not repeated; no `COMMIT2`, `ERASE`, reflash, executor reset or source-code change occurred.

The private COMMIT1 capture is 293 bytes with SHA-256 `3ff1084344e9b5af9e2a86f2902acf3158e017b86b699616a2b4bdc42b1a7a92`. The private RECOVER capture is 250 bytes with SHA-256 `4b68736cad4114033912d46465194804558a79ce392a8b98fc1f272bf015b40c`. Neither capture, payload, source, device identifier nor private path is published. Stage 6 remains unexecuted and requires separate explicit owner authorization.
