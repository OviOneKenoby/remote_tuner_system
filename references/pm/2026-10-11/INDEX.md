# PM reconciliation evidence - 2026-10-11
Input coordination main `531aa8cd0435ed9813ab39664888992583df0d28`; review UTC 2026-10-11T17:37:47Z.

[Technical reconciliation scope](../../PM_RECONCILIATION_SCOPE_2026-10-11.md) records technical objectives, allowed/excluded actions and integration commits; conversational transcript removed by administrative correction.

- [Integration heads/merge commits](INTEGRATION.json); [PR7](pr7_api.json), [PR8](pr8_api.json), [PR9](pr9_api.json) API snapshots. Issue comments, reviews and inline threads fetched independently: all empty at review.
- [Complete read inventory](read_inventory.json): PR7 5 files, PR8 35, PR9 47; every text decoded, JSON parsed, binaries inventoried.
- `python -B run_qualification.py` in each exported standalone prototype, Windows/Python3.13.13/Git2.55.0.windows.2. [A003 log](A-REMOTE-003/TEST_LOG.txt), [measurements](A-REMOTE-003/MEASUREMENTS.json), [matrix](A-REMOTE-003/FAULT_MATRIX.json); [A004 log](A-REMOTE-004/TEST_LOG.txt), [measurements](A-REMOTE-004/MEASUREMENTS.json), [matrix](A-REMOTE-004/FAULT_MATRIX.json).
- Rerun JSON matches originals except environment metadata; matrices and binary fixtures match exactly. All pinned evidence manifests verified against Git blobs. Five A004 vendor files byte-match PR8. Fake models do not import production Core/ESP SDK.
- [Release metadata](tuner-v1.1.11/release.json), [firmware PR5](tuner-v1.1.11/firmware_pr5.json), [main](tuner-v1.1.11/main.json), [tag](tuner-v1.1.11/tag.json), [source comparison](tuner-v1.1.11/source_to_release_compare.json), [all five asset digest checks](tuner-v1.1.11/ASSET_VERIFICATION.json).
- [Final validation](tuner-v1.1.11/FINAL_VALIDATION_RO.md), [TEST01](tuner-v1.1.11/TEST_01/HARDWARE_REPORT_RO.md), [SUSTAINED01](tuner-v1.1.11/SUSTAINED_01/HARDWARE_REPORT_RO.md) copied from pinned firmware merge. Original relative raw-log links resolve in [immutable original directory](https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/tree/5fb92c95d228d744d1182ae3956e850c5be2f277/artifacts/NETWORK_VALIDATION_1.1.11_PSRAM), not all copied here.
- [Build manifest](tuner-v1.1.11/BUILD_MANIFEST.md) retains stale candidate/OPEN header, superseded by FINAL_VALIDATION only as status. Original BIN/ELF distributed via release URLs, not duplicated here.
- [Validation record](VALIDATION.json): preserved evidence/archives, root manifest, active links/template fields. Root SHA256SUMS hashes Git blobs, excludes itself. Historical imported/archived relative links may resolve only at original location; no evidence edited to repair them.

No target build, flash, real NVS/credentials/partition operation or hardware test in this review. Hardware acceptance is prior pinned owner evidence, distinct from PM host reruns.
