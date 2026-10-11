# A-REMOTE-003: D0 complete-profile isolated codec/storage qualification

Delivery READY FOR REVIEW. Production qualification **FAIL / BLOCKED**. No firmware behavior change, live NVS access, production integration, build/upload/hardware test, Native approval or D1-D5 work.

Execution input coordination main `531aa8cd0435ed9813ab39664888992583df0d28`, task/package/rules/footer read at that input. A-002 reviewed design/source snapshots reused and byte-checked. Current device is Git-less C:/Users/RYZEN/Documents/REMOTE01/Code;4040 entry files inventoried; only prior local changelog differs from A-002 relevant baseline. Actual firmware commit and source/BIN/flashed correspondence UNKNOWN. Frozen CCM SHA7a46f9fffe706476de458aac078d0af1c94844df339248d3f9f4b5cf033011d7 unchanged.

## Deliverables and measured decision

[Evidence index](../references/device_evidence/remote/A-REMOTE-003/INDEX.md) links the full projection/field trace, exact schema/prototype/tests, fixtures/BINs, sizes/capacity arithmetic, faults, inventory and hashes. Standalone Python source is also in the device under tools/qualification/a_remote_003, outside components/main/CMake selection. No C++/production dependency added.

| Complete profile fixture | Encoded bytes | Decision |
| --- | ---: | --- |
| Typical unresolved effect+registry+two-binding conflict |2746|Fits3072 alone; not enough reserve |
| Same fixture after two full closure proofs |3228|FAIL3072 |
| Saturated supported pending input |35324|FAIL3072/current NVS |
| Saturated resolved input / derived legal maximum |44284|FAIL3072/current NVS |

Typical reserve482 bytes, maximum reserve8960. Profile permits exact128-byte IDs/256-byte text, retains complete captures/attempt/evidence/contract/keys/conflict roster; incompatible schemas/counts/extra proof growth refuse without dropping safety data. It explicitly blocks recipes/numeric/assets/seek/multiple attempts/partial-key proofs/ownership-changing associations and live scheduling. This is a narrowed host qualification profile, not all-CCM conformance or a production capacity promise. Maximum derivation exactly matches a legal encoded saturated fixture; full ledger shows each section and every sensitivity case.

## Verification and feasibility

`python -B run_qualification.py`:13 tests PASS;3859 counted checks;0 failures/errors. 87 fault scenarios (80 boundary combinations,6 explicit failures,1 counterexample);100 repeated fake update/recovery cycles. Canonical roundtrip and exact types; every typical-frame truncation; seeded512 corruptions; bounds/overflow/schema/migration; reserve/capacity; independent emission history, no recovery replay; historical proof/attempt preservation. Full result [TEST_LOG](../references/device_evidence/remote/A-REMOTE-003/results/TEST_LOG.txt). Python3.13.13/Windows11; seed30032026. No normal/soak firmware results relabeled as new tests; no target compile needed.

SDK5.5.3 source supports six126-entry pages/32-byte entries,4000-byte chunk optimistic ceiling and a20000-byte per-blob upper bound for this partition. Complete maximum cannot fit even singly. Peak offline model accounts for active+inactive+replacement banks, old/new anchors, synthetic credential old/new occupancy, metadata, GC and full proof reserve. Actual free NVS/other namespace data is UNKNOWN; no secrets inspected. No physical capacity/latency/endurance certification.

StrategyA failure: restoring an older valid SEALED anchor after independently observed new simulated emission makes older no-effect/allocator0 bank indistinguishable; tests expose lost latest-intent evidence. Missing/corrupt root already blocks. This is a model counterexample, not a demonstrated NVS physical bug. Complete guarantees cannot be certified from CRC/readback/nvs_commit. Detailed [fault report](../references/device_evidence/remote/A-REMOTE-003/FAULT_QUALIFICATION.md) provides exact failed fixture, source behavior and bounded rooted-chain/monotonic-head alternative, proposal only. No automatic older-bank fallback or semantic weakening.

## Remaining blockers and next gates

PM review required for complete profile/size and checkpoint strategy rejection. Separately assign bounded redesign and trusted newest-intent/non-reuse recovery qualification; actual free stats, fragmentation/GC, abrupt power-loss and durability/latency/frame evidence need controlled authorization. Target external proof validity/identity/context/ledger/fences and production import/session reset are not qualified by synthetic fixtures. D1-D5 stay unassigned; Native UNAPPROVED/UNFROZEN/NOT IMPLEMENTED, O01-O17 OPEN, common gate OPEN / NOT PASSED. No independent TUNER acceptance inferred.

Target flash/RAM/frame/task deltas=0 because no target-selected source changed; future target codec resource costs UNKNOWN. Existing .pio bytes preserved; no new firmware hashes/artifacts claimed. Hardware NOT RUN. Prior sleep rollback residency and source/flashed mismatch remain independent pending evidence. Complete handoff archived/replaced and publication is via result PR, never automatic merge.
