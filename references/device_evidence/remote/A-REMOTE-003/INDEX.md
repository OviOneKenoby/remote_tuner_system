# A-REMOTE-003 evidence index

Execution input current main531aa8cd0435ed9813ab39664888992583df0d28. Authorization: tasks/A-REMOTE-003.md and references/PM_FOLLOW_UP_A003_2026-10-08.md; mandatory footer observed. Git-less local inventory4040files; frozen/source/SDK identity checked against reviewed A-002. No production integration/live NVS/credentials access/build/upload/hardware test.

- [Report](../../../../reports/A-REMOTE-003.md)
- [Complete projection/profile/field-family trace](PROJECTION_PROFILE.md) / [every field path](results/FIELD_PATHS.md)
- [Exact measured size/capacity ledger](SIZE_CAPACITY.md) / [machine-readable measurements](results/MEASUREMENTS.json)
- [Fault qualification/counterexample/revised alternative/future proposal](FAULT_QUALIFICATION.md) / [87 scenarios](results/FAULT_MATRIX.json)
- [Test log](results/TEST_LOG.txt); command `python -B run_qualification.py` from prototype;13 tests/3859 counted checks/0 failures/errors,seed30032026
- [codec](prototype/codec.py), [fixtures](prototype/fixtures.py), [fake backend](prototype/backend.py), [tests](prototype/test_qualification.py), [reproduction runner](prototype/run_qualification.py)
- [Typical pending](results/typical_pending.json) / [binary](results/typical_pending.bin); [typical resolved](results/typical_resolved.json) / [binary](results/typical_resolved.bin)
- [Maximum pending](results/maximum_pending.json) / [binary](results/maximum_pending.bin); [maximum resolved](results/maximum_resolved.json) / [binary](results/maximum_resolved.bin)
- [Baseline](BASELINE.json) / [full entry inventory](ENTRY_SHA256.json) / [scope validation](SCOPE_VALIDATION.json)
- [Local device report copy](DEVICE_QUALIFICATION.md) / [local delivered file hashes](DEVICE_DELIVERY_SHA256.json)
- [Validation](VALIDATION.md) / [evidence file hashes](EVIDENCE_SHA256.json)
- Immutable source/SDK anchors: [A-002 index](../A-REMOTE-002/INDEX.md). New production files/artifacts NONE.

Host assertions PASS; production strategyA/3KiB/current-storage complete-profile qualification FAIL/BLOCKED. Physical NVS behavior/resources UNKNOWN, hardware NOT RUN. These are useful failed qualification results, not accepted production recovery. Namespace isolation is not capacity isolation.
