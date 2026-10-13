# A-REMOTE-010 Stage 5 first-record authorization

Recorded 2026-10-13. The owner accepted Stage 4 and authorized exactly one `!A010 COMMIT1 CONFIRM-A010-REMOTE-CTL-COMMIT1`, followed by the proven owner-operated normal hardware reset and exactly one read-only `!A010 RECOVER`.

The required transition was initialized-empty generation 0 to valid generation 1, next generation 2 and no incomplete transaction, preserved across reboot with functional UI and retained configuration. The prior USB-JTAG reset sequence was prohibited. Repeating `INIT` or `COMMIT1`, executing `COMMIT2` or `ERASE`, reflashing and source-code changes were prohibited. Execution had to stop before Stage 6.
