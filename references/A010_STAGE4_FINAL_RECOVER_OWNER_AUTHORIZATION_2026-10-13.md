# A-REMOTE-010 Stage 4 final recovery authorization

Recorded 2026-10-13. The owner reported performing a normal hardware reset out of ROM download mode and confirmed that the UI was functional. The owner authorized verification of the running diagnostic firmware followed by exactly one read-only `!A010 RECOVER`.

The required recovered state was initialized-empty, generation 0, next generation 1 and no incomplete transaction. Repeating `INIT`, flashing, erasing, source-code changes and additional resets were prohibited. Successful verification would complete Stage 4 and execution had to stop before Stage 5.
