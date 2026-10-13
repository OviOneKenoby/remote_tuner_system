# A-REMOTE-010 Stage 3 read-only UART authorization

Recorded 2026-10-13. The owner authorized the published protocol's Stage 3 against the installed diagnostic candidate, limited to sending `!A010 INFO` and `!A010 STATUS` through the established USB-serial connection.

The required checks were the exact `remote_ctl` partition identity, erased state, generation 0, absence of unexpected errors and absence of payload disclosure. Firmware flashing and source-code changes were prohibited. `INIT`, `COMMIT1`, `COMMIT2` and `ERASE` remained prohibited.
