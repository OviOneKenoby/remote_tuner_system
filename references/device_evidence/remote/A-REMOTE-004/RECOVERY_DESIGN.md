# Bounded typed recovery/compaction and required backend guarantees

Implemented ONLY as Python standalone qualification and fake storage. No production Core import,NVS API,credential access or hardware. Historical data is never a replay queue. Canonical profile is PROFILE_AND_TRACE.md.

## Required guarantees G1-G4 (ASSUMED in qualified fake,NOT proven for NVS)

Prerequisite G0:exactly one serialized writer and no reentrant publication/deletion. This follows the current Core owner design (Store/Memory owner comments,Core::begin guard),but production integration is not tested here. Fake append/compact guards reject reentry before mutation;CAS alone cannot make concurrent inactive-segment deletion safe. No multi-writer guarantee is claimed.

G1: durable atomic monotonic trusted-head compare-and-swap/read. Every acknowledged successor remains newest across restart;old valid head cannot become current after acknowledgement. Missing/unavailable/integrity failure is detectable and blocks. This service must be outside the rollbackable record domain or have independently QUALIFIED recovery semantics. CRC/hash/readback,nvs_commit,an ordinary generation value in the same rollbackable blob,or a boolean flag cannot establish G1. `qualified=True` is an explicit HOST ASSUMPTION,not evidence from hardware.

G2: all acknowledged record writes that a published head references are durable BEFORE head acknowledgement and stay readable until explicitly erased as unreachable. Head publication orders preceding storage writes;ambiguous write/root outcomes may leave prior/new state,but cannot acknowledge a head referencing incomplete bytes. Missing/CRC/hash/correlation mismatch blocks. Real setters/flush ordering/power-loss behavior need separate qualification.

G3: root CAS failure/ambiguous acknowledgement preserves complete OLD OR NEW trusted head;never invents an acknowledged generation or undetectable head corruption. Strict monotonic generation/record sequence and exact expected-root comparison serialize publication. Counters cannot wrap. Actual fixed76byte atomic root service implementation and resource/endurance cost are UNKNOWN;fake is not its implementation.

G4: bounded quota,GC and safe deletion guarantees. Only inactive/unreachable records may be deleted before replacement;delete completion/reuse does not alias live keys. Preflight reserves both complete snapshots,all remaining proof growth,tail allocations and update/compaction overlap;no active barrier/tombstone/proof eviction. Namespace isolation is not partition-capacity isolation. Physical fragmentation/other occupancy/root metadata may invalidate the optimistic budget.

None of G1-G4 is hardware accepted. Actual/unqualified backend mode ALWAYS returns GLOBAL_BLOCK before mutation/emission,even with valid bytes. Re-establishing these guarantees cannot be asserted by setting a software flag.

## Typed records and fixed bounds

BASE carries the complete P4 state,maximum6383+64=6447bytes. ALLOC carries all10allocator counters,exactly162bytes including node64 and typed payload98;only the next paired lifetime/ticket advance may differ. PROOF carries full normalized AdapterEvidence body,maximum1146bytes including node64;append retains the original full evidence and derives independent per-key states only for exact historical correlation. Record header64bytes:C4LR/version/type/features,UInt64sequence/generation,previous-recordSHA256,payload length/CRC. Root76bytes:C4RT/version/features,generation,first/lastsequence,segment/tailcount,head digest,CRC. Hash chain correlates bytes and sequence;it does NOT prove newest intent or authenticity.

Two fixed segments,each BASE+four tail keys;only one active. Every operation starts from a validated current trusted head. Tail ordering and head digest cover exact contiguous referenced records;unknown/missing/stale/malformed referenced record blocks,no older-bank fallback. Extra unreachable orphan nodes are not authority and cannot emit. Zero dynamic log growth;proof slots reserved before allocations. Compaction is explicit when allocation would spend remaining proof slots or tail is full. Four deleted IDs are preserved,not evicted to make space.

## Append / crash-safe compaction CONDITIONAL on G1-G4

Append preflights candidate+full future reserve,validates exact typed transition,first removes inactive old BASE/tail left by interrupted post-CAS cleanup,then only an unreachable failed-write orphan at next fixed key,writes/commits/readbacks complete node,then monotonic CAS publishes new head. Ambiguous failure stops;recovery sees old or complete new history,or blocks. Capacity refusal cannot become a new executable success. Fake commits intentionally add no atomicity (matches installed handle source).

Compaction reconstructs ALL mandatory state from active BASE+tail;captures current trusted root;erases only inactive/unreachable segment;writes complete BASE there;commit/readback;CAS to new generation/sequence/segment;then erases old segment. Before CAS,current segment stays sole authority. After CAS,new complete BASE is sole authority,even if cleanup fails. No second active tail accumulates after interrupted cleanup:the next append first cleans the entire inactive segment,and a focused regression covers this reserve obligation. Two BASE generations overlap,not three:stale inactive blob/version is removed BEFORE replacement;unknown cleanup/readback error aborts safely. No live history may be omitted. Host tests cover every concrete before/after read/write/commit/CAS/emission/erase boundary and intermediate per-key proof during compaction.

Fake initial history handover uses a complete worst-case correlated effect projection plus consumed pair BEFORE independent simulated emission. It is not an implementation/test of Core admission,scheduler,deadline/target-side semantics or real execution. Production pre-handover mapping and old-result retirement remain blocked and require a separate assignment.

## Counterexamples retained

A003 valid-old-anchor counterexample is reproduced against byte-original vendor backend:one independent simulated emission can coexist with older no-effect/allocator0 decoded state. A004 ordinary-record rollback with NEW trusted head intact => GLOBAL_BLOCK. Stale root-CAS expected bytes => refusal. Entire trusted head+data rollback deliberately violates G1 and reproduces an undetectable older no-effect state after emission. No hash chain can distinguish it. This is an information/guarantee limitation,not a physical NVS defect demonstrated here. Since actual G1 is unqualified,production remains BLOCKED.

## Reconciliation prerequisites if newest intent cannot be recovered

Remain GLOBAL_BLOCK over the registry/bindings/targets/resources whose scope cannot be established,not just keys from an older valid snapshot. Obtain trusted complete newest history or independent verified no-future-execution fencing/reconciliation over ALL possibly affected attempts/resources. Readback/current state/reconnect/timeout/priority cannot prove no past execution or clear barriers. Allocation/lifetime identity is a separate obligation:fencing alone cannot restore non-reuse. Restore a trustworthy monotonic allocator/registry identity domain;any new-domain/reprovision/reset policy requires explicit design/owner approval and must not forward stale IDs. Reverify current target identity/mapping/context/security/session and discard old scheduling/current observations;never recreate old full results. No reconciliation implementation or target protocol is added here.

Future qualification must first define exact fault/threat model (power loss vs adversarial flash restoration),inspect candidate head service and measure sanitized free stats/GC/latency/resources,then separately authorized synthetic isolated physical power-cut/NO_SPACE testing. Do not test on live credentials or flash automatically. A larger partition helps sizing only,not G1. D1 remains unassigned;Native/O01-O17/common gate unchanged.
