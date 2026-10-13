# A-REMOTE-010 Stage 4 initialization authorization

Recorded 2026-10-13. The owner authorized one execution of `!A010 INIT CONFIRM-A010-REMOTE-CTL-INIT`, followed only after the required transition by `!A010 STATUS`, one REMOTE reboot and `!A010 RECOVER`.

The required state was erased to initialized-empty, generation 0 and next generation 1, persistent across the reboot with normal existing UI/configuration. `COMMIT1`, `COMMIT2`, `ERASE`, firmware reflashing and source-code changes were prohibited. Any unexpected result required an immediate stop, and a failed mutation could not be retried.
