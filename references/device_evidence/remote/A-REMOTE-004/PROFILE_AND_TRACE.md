# A-REMOTE-004 complete minimum useful supported profile and trace

INTERNAL QUALIFICATION PROFILE ONLY. Frozen CCM1.0.0 unchanged;no Native capacity promise or production importer/journal. All represented safety fields are retained exactly,with lossless schema-driven interning. No raw Store,pointer/ABI dump,digest-only proof or silent truncation. This is useful for one unresolved Favorite activation plus historical two-route conflict recovery,not a general-purpose durable Core.

## Profile P4,exact bounds/refusal

| Domain | Bound | Authority/distinction |
| --- | --- | --- |
| Registry/device/target |1 each| internal profile;CCM2/4 identities and all applicable generations retained |
| Bindings/resource |2 bindings,1 shared resource| permits cross-route conflict and TARGET+actual RESOURCE barriers;CCM12/17 |
| Favorite catalog |1 catalog,2 items| full original SelectionRef/private token/captures;CCM6/15 |
| Effect/attempt |1 closed ambiguous DEVICE_NATIVE Favorite history,1 attempt| full request/attempt/contracts/errors/progress retained;CCM10-13 |
| Conflict |1 media.title roster,2 participants| full conflict/start ingress and historical StateObservations retained;CCM8/9 |
| Deletion identities |<=4 scoped tombstones| no active identity eviction or reuse;CCM2 |
| ID syntax/length |1-128 ASCII [A-Za-z0-9._:-]| actual frozenCCM2 and current Id;not a reduced ID cap |
| Text |<=64 UTF-8 bytes| narrower than general CCM/current Text;explicit supported profile,never truncate |
| Evidence/contract |<=1 verified claim per full Evidence,<=1 guaranteed-no-execution error entry per full contract| full kind/reference/version/claim retained;larger records refuse before hypothetical handover |
| Other lists |identity/mapping/resource/catalog evidence<=1,provenance<=4,precondition<=1,route<=1,resource<=1| narrowed existing closed schemas;no dropping data to satisfy these bounds |
| Proofs |initial PROGRESS + <=1 FUTURE_FENCE + <=1 NO_EXECUTION,each with full exact TARGET+RESOURCE coverage| full proof bodies and independent past/future state;either arrival order;intermediate state survives compaction |
| Unique string dictionaries |pending IDs<=30/TEXT<=10;one extra proof31/13;two proofs32/16| full byte equality reuse only;reserve one new evidenceID+3new texts per proof;historical error/progress unchanged |
| Physical log |one active snapshot +<=4 ALLOC/PROOF records,two segment slots| remaining two/one proof slots cannot be spent on allocation updates;compact first |

No association transaction/history is supported:nonempty association history refuses import/handovers requiring it. No object reassociation,identity merge/removal,recipes/numeric/URI/content/seek/assets/multiple effects/attempts/retries/alternate routes,partial-key proof coverage,exclusion evidence or arbitrary capability mutation. Existing broader state must BLOCK,not be projected by deleting mandatory fields. The codec's closed schema names every blocked optional field;unknown input fields/tags/versions reject. Production admission/import gates are NOT IMPLEMENTED.

The two proof kinds may arrive independently,in either order. Past-only proof leaves no_future=false and whole-attempt guaranteed_no_execution=false. Future-only fencing leaves no_past=false. Neither restarts scheduling or changes historical delivery/emitted lower bounds. Full resolution preserves exact request,attempt captures/deadline/first-terminal,contract,old error,conflict roster and provenance. Every proof is retained in full and also in Attempt.evidence;interning removes repeated bytes,not semantic fields. A verified target proof is not established by these synthetic PROJECT_DESIGN fixtures.

Future-proof payload bounds/coverage must be a VERIFIED adapter contract before any real handover. No actual target has that qualification here. Oversized/out-of-contract late evidence remains a reconciliation blocker,never grounds to discard prior safety state or pretend resolution. Extra valid proof events/partial coverage require a larger separately qualified profile. Allocated refusal-pairs consume lifetime/ticket through a typed durable ALLOC record;record/head/generation UInt64 exhaustion refuses,never wraps. Arbitrary registry changes are blocked;all namespace allocator metadata and existing scoped deleted IDs remain in snapshots and compaction.

## Exact canonical encoding

C4SC frame16bytes:magic/version1/features0/payload length/CRC32. Two sorted unique byte dictionaries,one for IDs and one for TEXT,each has u8count and u8byte-length entries. All scalar strings are schema-typed u8indexes. All other fields preserve A003 canonical little-endian typed encoding,closed enum/tag/bool,u16 ordered list counts,exact integer/rational semantics. Re-encode equality rejects noncanonical,unused or duplicate dictionary entries. No general compression/ABI dependence. UTF-8 and ID validation remain explicit.

Core request IDs are currently `intent:` + unsigned checked lifetime sum (core.cpp1237-1253),maximum27bytes;other IDs remain128. Epoch/lifetime/current-watermark/pair metadata preserve exact integers. IDs are not normalized or interpreted outside this existing Core allocation convention. Target compiler padding never enters encoding.

## Maximum legal state,not a sample estimate

Runner recursively derives maximum typed body using narrowed schema counts,then deducts enforced title STRING vs larger REFERENCE,RESOURCE second key,absent seek/recipe/step fields. It adds saturated30/31/32 ID entries (all128bytes except generated intentID27),10/13/16 distinct64byte texts,table headers and frame. The generated legal fixtures attain5587/5985/6383bytes exactly. Two future proofs reserve796 total bytes (398 each) in the full state. Log proof nodes have separate dictionary/record overhead and require1146bytes each,not398.

## Field-by-field trace,mandatory coverage and intentional blocking

[Full field-path list](FIELD_PATHS_FROM_A003.md) retains every leaf,optional/tag branch and list. [Pinned A003 complete trace](https://github.com/OviOneKenoby/remote_tuner_system/blob/74e4f1a681cd589625aff63e91f917076cc22586/references/device_evidence/remote/A-REMOTE-003/PROJECTION_PROFILE.md) maps all those fields to frozen clauses and current source types;P4 changes only the declared bounds above and adds intermediate proof validation. Association paths remain explicitly blocked,not omitted from supported inputs.

| Field family | CCM | Current inspected source | A004 preservation/recovery |
| --- | --- | --- | --- |
| format/features/model/registry/allocators/deleted IDs |1,2,10,12| core.hpp Store;core.cpp expected_id/allocate;model.hpp Version/Id | exact metadata in BASE;ALLOC can change only next lifetime/ticket pair;others immutable |
| epoch/ingress/generations |2,3,12,18| Store.clock_epoch/ingress/watermark/epoch_base;Core constructor231-253 | retain historical scopes;new-epoch boot/import is NOT implemented;no generation rollback |
| devices/targets/bindings/resources |2,4,16,17| CommonDevice/Target/Binding/SharedResource | full safety identity/gen/versions/evidence/refs/membership/order retained;non-safety labels not serialized |
| catalogs/items |6,15| CatalogRecord/CatalogSnapshot/SelectionRef | exact catalog/token generations and immutable Favorite refs/label/variant/private opaque tokens |
| conflict/participant/resync observation |3,8,9,18| ConflictState/ConflictParticipant/StateObservation | full roster/watermarks/typed values/provenance/time/sequence/context retained as HISTORICAL;current selected state not restored |
| effect request/route/preconditions/attempt |10-13,17| CommandRequest/StepCapture/RouteCapture/Attempt | every supported field exact;unsupported recipes/steps explicitly blocked;no old scheduling/result recreation |
| contracts/retry/semantic/error/progress/closure |6,10-13| ExecutionContract/RetryPolicy/Error/Record/Effect | full original content;no fallback/current-descriptor substitution or terminal reopening |
| effect keys/past/future/proof history |11,12,17,18| EffectKey/AdapterEvidence/Effect.evidence_ids | full proof beyond existing evidenceID-only storage;validate historical correlation and actual keys before appending |
| association/other operation fields |6,14-16| broader model structs/current schemas | BLOCKED for this profile,not silently removed |

Production pointers/queues/adapter routes/tasks never persist. Current authorization/reachability/contact/capability schemas/state samples/optimistic overlays are UNKNOWN/empty after modeled recovery and must be reverified. Full old-epoch dedup/scheduling and old result recreation are not supported. Recovered typed history is always HISTORICAL_ONLY_BLOCKED;GLOBAL_BLOCK if newest history cannot be established. Frozen safety/model semantics are not changed by a smaller supported profile. Source/frozen/SDK hashes are in SOURCE_SDK_SHA256.json;actual firmware commit/flashed correspondence UNKNOWN.
