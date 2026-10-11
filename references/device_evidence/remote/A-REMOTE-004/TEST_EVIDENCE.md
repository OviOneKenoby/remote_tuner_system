# Isolated host qualification results

Command:`python -B run_qualification.py` in prototype. Environment:3.13.13 / Windows-11-10.0.26200-SP0. Seed40042026. PASS:12tests,7805explicit counted checks,0failures/errors. 562recorded scenarios. Full test log,fixtures,BINs,recursive size bounds and matrix in results/. No production normal/soak/target build/hardware evidence relabeled as new results.

| Scenario family | Count |
| --- | ---: |
| A003-counterexample | 1 |
| G1-contract-violation | 1 |
| initial-history-handover | 152 |
| future-proof | 120 |
| refused-allocation | 136 |
| compaction-with-live-barrier | 152 |

560 interrupted boundary cases cover every actual before/after read,write,commit,root CAS,erase and independent fake emission boundary in initial history checkpoint,proof append,allocation update and compaction with a live intermediate barrier. Modes stop/torn/lost/ambiguous are abstract injected outcomes;not every mode at a read/CAS implies a separate physical mechanism. A003 valid-old-anchor counterexample and deliberate G1 trusted-service+records rollback add2cases. Qualified-model recovery either keeps verified historical data or GLOBAL_BLOCK;it NEVER receives an oracle/adapter or emits. Independent oracle emission list is not derived from codec output.

Other focused tests cover every6383byte maximal frame truncation,512seeded bit flips,unknown format/features/downgrade,bounds/closed keys/UTF8/schema,dictionary reserve limits,full immutable roundtrip,actual TARGET+RESOURCE/proof correlation,no active eviction,proof arriving in either order,non-reuse/generation/record-sequence exhaustion,explicit write/commit/read/CAS errors,reentrant writer refusal and quota failure. 100 repeated compactions with400allocation advances preserve exact original effect/proofs/conflict/IDs and emit nothing.

A focused post-CAS cleanup-interruption regression proves the next append removes the entire inactive old BASE/tail before accumulating another active tail. Without that cleanup,the single-tail peak reserve would not cover both tails. This is a prototype-design correction found during host qualification,not a discovered firmware defect. All actual firmware remains unchanged.

Host PASS is CONDITIONAL on G0serialized ownership and assumed G1-G4backend guarantees. Actual ESP/NVS newest-head integrity/free-space/durability/endurance/latency remain unqualified. Default unqualified fake blocks even valid bytes. Whole trusted-backend rollback is explicitly undetectable ifG1is violated;no cryptographic anti-rollback claim. Production remains BLOCKED. Physical hardware NOT RUN.
