# Compatibility, migration and future task boundaries
PROPOSED / NOT APPROVED. No current device task assigned. Owner approval of the exact threat-model diff permits scheduling only the scoped analysis/host tasks below against a newly published approved revision; it does not approve Native, physical operations, partition writes or production firmware.

| Prospective exact task ID | Scope after contract approval and explicit PM assignment | Completion gate |
| --- | --- | --- |
| A-REMOTE-006 | Design exact append/root commit/recovery state machine and isolated host G1a model; reclassify G1b OUTSIDE; retain all mandatory data | Independent emission oracle, complete fault matrix, no-replay/allocator/barrier proof; still no production |
| A-REMOTE-007 | Exact complete codec/profile/capacity and partition/migration design only; compare enforced bounds against48KiB recommendation | Lossless encoded maxima/overlap/proof growth/GC/remote_wifi/fragmentation/unknown schema refusal; owner accepts layout before any write |
| A-REMOTE-008 | Synthetic sacrificial-board NVS qualification only under separately approved board/layout/destructive test authorization | Actual SDK ordering/ack/power-cut/GC/capacity/latency/endurance evidence and independent witness; never live credentials |
| A-REMOTE-009 | Production durable backend integration only after006/007/008 acceptance and separate exact device assignment | Core safety regressions, versioned schema migration, actual device acceptance; no Native/TUNER expansion |

These IDs are reserved proposals, not assignments; dependencies do not auto-dispatch. D1-D5 remain unassigned. TUNER implementation tasks: NONE under this proposal.

Publish a new approved CCM revision only after exact diff and both reviews are accepted by owner, preserving1.0.0 artifact/approval history. Proposed semantic delta is REMOTE operational threat scope only; no wire/type/command changes. Existing1.0.0 implementations do not gain conformance automatically. Capability/profile/version mismatch must be explicit, never negotiated as Native support. Migration cannot infer a safe accepted history from current in-memory MockJournal or an unknown old schema. If no trusted complete source exists, keep affected scopes blocked pending explicit reconciliation/fencing; do not fabricate barriers or clear allocator history.

Migration design must name source/destination schemas, explicit version gate, verified lossless conversion, space for source plus destination, interrupted-step recovery/rollback, and independent no-emission checks. Unknown versions/corruption/incomplete root relationships fail closed. Partition changes require a separately reviewed layout avoiding existing offsets and preserving all mandatory data, backup/recovery and separately authorized hardware execution. This PR changes no device file or historical/latest handoff.
