# A-REMOTE-004: Bounded recovery redesign and isolated qualification

Delivery READY FOR REVIEW. **Conditional host qualification PASS;actual backend/capacity production qualification BLOCKED.** No production Core integration,live NVS/credential access,partition/configuration change,build/upload/hardware or Native implementation/approval. PR8 remains separate;no merge performed.

## Authority and baseline

Current coordination main read531aa8cd0435ed9813ab39664888992583df0d28. Direct owner authorization is preserved in [task](../tasks/A-REMOTE-004.md);authorization first published on this separate result branch before prototype work. Exact A003 input74e4f1a681cd589625aff63e91f917076cc22586/[PR8](https://github.com/OviOneKenoby/remote_tuner_system/pull/8) reviewed and preserved,including full profile,size ledger and stale-valid-anchor counterexample. Immutable vendor copies/hash manifest retain that host input. Device C:/Users/RYZEN/Documents/REMOTE01/Code is Git-less;4047entry files inventoried;A003 relevant executable/config/tests/artifacts unchanged. Current firmware commit/source/flashed correspondence UNKNOWN. Frozen CCM hash unchanged.

## Implemented standalone design

[Profile/trace](../references/device_evidence/remote/A-REMOTE-004/PROFILE_AND_TRACE.md):one device/target,two bindings,one resource,two Favorites,one full unresolved effect/attempt and two-route conflict,all mandatory captures/IDs/contract/proofs/past-future keys/non-reuse metadata. Explicit64byte text and bounded evidence/dictionary profile rejects unsupported data BEFORE hypothetical handover;no safety field truncation. Association/recipes/numeric/assets/multiple effects/partial-key coverage unsupported,not silently discarded. Future proof types/size/coverage still require a verified target contract before production work.

Lossless typed string interning plus BASE/ALLOC/PROOF records. Complete intermediate past-only/future-only states persist independently. Two segment slots,four tail records,future proof slots reserved. [Recovery/compaction](../references/device_evidence/remote/A-REMOTE-004/RECOVERY_DESIGN.md) writes complete new BASE before monotonic trusted-head CAS,then cleans old segment;next append removes interrupted inactive cleanup before another tail accumulates. Full barriers/rosters/proofs/allocators retained,no replay or old result reconstruction.

Trusted-head backend G1-G4 are explicit assumptions,NOT proven from hash/readback/nvs_commit. Single serialized writer required. Default unqualified backend returns GLOBAL_BLOCK. Tests reproduce A003 counterexample and show whole trusted-service rollback remains undetectable ifG1violated. Ordinary-record rollback with newest trusted head intact blocks. Reconciliation requires verified scope-wide fencing plus independent allocator/identity non-reuse restoration;neither current state nor fencing alone proves a lost allocation watermark. No real head backend selected or implemented.

## Exact measurements / current-partition verdict

| P4 complete state | Encoded maximum |
| --- | ---: |
| Pending |5587bytes|
| One extra proof |5985bytes|
| Two-proof resolved |6383bytes|

Maximum future state growth796bytes. Exact node maxima:BASE6447,PROOF1146,ALLOC162;root76. Peak raw record reserve15510bytes (two BASE generations,two proofs,two allocations);saturated modeled compaction measured14390bytes. Recursive legal maximum matches constructed saturated fixtures exactly;[ledger](../references/device_evidence/remote/A-REMOTE-004/SIZE_CAPACITY.md) includes all dictionary/record/header/update/compaction/proof overhead.

Existing24KiB NVS has756entries. SDK-backed optimistic peak includes old/new roots,metadata,GC and synthetic old/new other occupancy:650entries at0bytes;686at512;718at1024;782at2048;912at4096. Thus CONDITIONALLY PLAUSIBLE only in smaller ideal cases,FAIL at2?4KiB;actual free space/fragmentation/root overhead UNKNOWN => production capacity BLOCKED. No credentials/stats were read. 32/48KiB are documented arithmetic alternatives only;no layout change,existing NVS cannot just expand over PHY/factory. More capacity does not solve newest-intent integrity.

## Tests and scope

`python -B run_qualification.py`:12tests PASS,7805counted checks,0failures/errors;562scenarios (560before/after fault cases +2counterexamples),fixed seed40042026;100compactions/400allocation updates;everymax-frame truncation/512corruptions. [Test evidence](../references/device_evidence/remote/A-REMOTE-004/TEST_EVIDENCE.md),[log](../references/device_evidence/remote/A-REMOTE-004/results/TEST_LOG.txt),[index](../references/device_evidence/remote/A-REMOTE-004/INDEX.md). Python3.13.13/Windows11. Host prototype runs only fake storage/independent simulated oracle;no real dispatch or Core admission/scheduler conformance claimed.

Local changes:new isolated tools/qualification/a_remote_004/prototype (including pinned vendor),docs/A_REMOTE_004_STORAGE_RECOVERY_QUALIFICATION.md,append-only CHANGELOG. Coordination changes:new task/report/evidence,own complete handoff and byte-original archives,append-only CHANGELOG and publication checksum/own evidence-byte preservation metadata. PM/TUNER files untouched. Source/tests/config/.pio preserved;no target-selected files changed,so target flash/RAM/frame delta0;future implementation costs UNKNOWN. No firmware normal/soak/build/upload or hardware.

## Remaining guarantees and next action

PM review:bounded profile/refusal/future-proof contract and backend proposal. Separately qualify a concrete newest-intent head service and ordered durable record/GC semantics;sanitized free-space/root overhead/latency/endurance and controlled synthetic physical power-cut tests require authorization. Actual importer/boot epoch/session/dedup retirement/current-auth revalidation and target-proof validation remain NOT IMPLEMENTED. No D1integration until these gates. Native UNAPPROVED/UNFROZEN/NOT IMPLEMENTED,O01-O17 OPEN;common gate OPEN/NOT PASSED. Historical firmware/flashed mismatch and pending sleep rollback evidence unchanged. Hardware NOT RUN.
