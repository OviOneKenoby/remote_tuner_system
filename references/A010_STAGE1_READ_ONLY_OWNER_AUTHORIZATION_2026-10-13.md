# A-REMOTE-010 Stage 1 read-only owner authorization

Recorded 2026-10-13. The owner authorized Stage 1 of the published A-REMOTE-010 hardware-validation protocol for diagnostic candidate publication commit `a1f7b3bb69b4bfa3823c3ba3c5a27c0958a4ab85`.

Authorized operations were limited to current COM-port discovery, device and physical-flash identification, and read-only inspection of the installed partition table, the dedicated `remote_ctl` region and current factory image. Firmware flashing, NVS initialization, flash or partition erasure, and every mutating diagnostic command were prohibited. Execution had to stop after Stage 1; implementation and test scope could change only if a real issue was identified.
