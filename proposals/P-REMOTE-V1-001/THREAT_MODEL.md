# Threat model and gate mapping
PROPOSED / NOT APPROVED. Frozen G1 and A005 verdict remain historical unchanged. New labels apply only if approved as a new revision.

| Event / requirement | Proposed classification | Required outcome |
| --- | --- | --- |
| Power-loss at every write/commit/GC boundary, torn/incomplete write | G1a REQUIRED | Recover determinable committed history or block affected scopes; zero recovery dispatch |
| Detectable corruption, stale root with newer/retained records, partial rollback | G1a REQUIRED | Validate root/generation/record correlation; ambiguity blocks, no silent older-root acceptance |
| Ambiguous setter/commit result before or after durable write | G1a REQUIRED | No optimistic acknowledgement/emission; retain unresolved barriers |
| Request/effect/barrier correlation and allocator non-reuse | G1a plus unchanged CCM REQUIRED | Preserve accepted history, no ordinary power-loss replay |
| Capacity exhaustion/proof growth/GC fragmentation | Unchanged capacity gate REQUIRED | Refuse before emission without truncation or mandatory eviction |
| Unknown schema or interrupted migration | Unchanged migration gate REQUIRED | Explicit migration or fail closed; zero emission |
| Whole NVS intentionally restored / old internally valid flash clone | G1b OUTSIDE V1 THREAT MODEL | No semantic survival or detection guarantee; never NVS PASS |
| Root and all records rolled back coherently by adversary / whole-flash rewrite | G1b OUTSIDE V1 THREAT MODEL | Report exclusion, not successful anti-rollback |
| Logical association rollback, reset/deletion, fencing/reconciliation | Unchanged CCM REQUIRED | New higher generations, retain historical barriers; no reexecution |

Old G1 combines newest committed-state freshness and adversarial coherent-domain anti-rollback. Exact map: operational freshness/partial mutations -> G1a REQUIRED; complete coherent intentional persistent-domain restoration -> G1b OUTSIDE. G0 serialization/CAS remains conditional/unqualified, physical G2 ordering, G3 durable acknowledgement and G4 capacity remain UNKNOWN; no renumbering/removal or retroactive PASS. A005 stale-root counterexample still fails G1a if blindly accepted. Its authentic whole-domain rollback counterexample demonstrates the exclusion, not a fix. Host tests need reclassification plus fresh G1a oracle tests before a new backend verdict.
