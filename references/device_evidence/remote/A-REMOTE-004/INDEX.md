# A-REMOTE-004 reproducible evidence index

Input main531aa8cd0435ed9813ab39664888992583df0d28;A003input74e4f1a681cd589625aff63e91f917076cc22586/PR8OPEN/UNMERGED. Direct owner authorization/task publication;no production integration/live NVS/credentials access/build/upload/hardware.

- [Task](../../../../tasks/A-REMOTE-004.md) / [report](../../../../reports/A-REMOTE-004.md)
- [Complete profile/trace](PROFILE_AND_TRACE.md) / [every inherited field path](FIELD_PATHS_FROM_A003.md)
- [Bounded records/recovery/compaction/guarantees/reconciliation](RECOVERY_DESIGN.md)
- [Exact size/peak capacity ledger/alternatives](SIZE_CAPACITY.md) / [machine-readable measurements](results/MEASUREMENTS.json)
- [Test classifications](TEST_EVIDENCE.md) / [log](results/TEST_LOG.txt) / [562scenarios](results/FAULT_MATRIX.json)
- [Projection codec](prototype/projection.py) / [fake typed protocol](prototype/protocol.py) / [tests](prototype/test_redesign.py) / [reproduction runner](prototype/run_qualification.py)
- [Pinned A003 input hashes](A003_INPUT_SHA256.json);immutable full modules under prototype/vendor_a003;A003published evidence remains unchanged at its pinned commit
- [Typical pending](results/typical_pending.json) / [binary](results/typical_pending.bin);[typical resolved](results/typical_resolved.json) / [binary](results/typical_resolved.bin)
- [Maximum pending](results/maximum_pending.json) / [binary](results/maximum_pending.bin);[maximum intermediate](results/maximum_intermediate.json) / [binary](results/maximum_intermediate.bin);[maximum resolved](results/maximum_resolved.json) / [binary](results/maximum_resolved.bin)
- [Baseline](BASELINE.json) / [4047file entry inventory](ENTRY_SHA256.json) / [source+SDK SHA](SOURCE_SDK_SHA256.json)
- [Scope validation](SCOPE_VALIDATION.json) / [local delivery hashes](DEVICE_DELIVERY_SHA256.json) / [local report copy](DEVICE_REPORT.md)
- [Archive provenance](ARCHIVE_PROVENANCE.json) / [validation](VALIDATION.md) / [evidence hashes](EVIDENCE_SHA256.json)

Run `python -B run_qualification.py` inside prototype;Python3.13.13/Windows11,seed40042026.12tests/7805countedchecks/0failures/errors;100compactions/400allocationupdates. Conditional host PASS does NOT qualify actual backend/newest-intent/capacity. Production BLOCKED,hardware NOT RUN. Native/O01-O17/common gate unchanged.
