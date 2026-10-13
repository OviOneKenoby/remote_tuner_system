# A-REMOTE-010 Stage 4 recovery-continuation authorization

Recorded 2026-10-13. The owner authorized a limited continuation after successful initialization. Repeating `INIT` was prohibited.

The authorized sequence was to determine whether REMOTE was running normally and whether the prior reset occurred; if still unverified, perform one controlled hardware reboot, re-establish USB serial, confirm normal boot, then send exactly one read-only `!A010 RECOVER`. The required recovered state was initialized-empty, generation 0, next generation 1 and no incomplete transaction, with normal UI and retained configuration. `COMMIT1`, `COMMIT2`, `ERASE`, firmware reflashing and source-code changes were prohibited. Execution had to stop before Stage 5.
