# D0 safety projection: isolated qualification profile 1

This is a project-internal, explicitly narrowed codec profile, not Native API support, a production journal, or complete frozen-CCM conformance certification. Frozen CCM1.0.0 is unchanged. The complete serialized field list is [FIELD_PATHS](results/FIELD_PATHS.md); this file assigns every path there to a clause/source family below. All fields are mandatory unless explicitly optional/tagged. Unknown keys, tags, formats/features and overflow refuse; no ABI/pointer/raw Store dump. No digest replaces an envelope, contract or proof: SHA/CRC only detect storage mismatch/corruption, not authority or newest-generation integrity.

## Exact supported bounds and refusal points

One registry/device/target, two current bindings, one shared resource, one Favorite catalog with two items, one closed ambiguous DEVICE_NATIVE Favorite activation/attempt, one media.title conflict with two participants; four deletion records, one completed same-owner TARGET association rollback record. IDs obey CCM1-128 ASCII bytes. Generic text is narrowed to <=256 UTF-8 bytes; larger otherwise-legal CCM text is refused, not shortened. Evidence has <=4 claims, contracts <=2 no-execution errors, mapping/identity/resource/catalog/association evidence <=1, provenance <=4 hops, one precondition, one route, one resource, no fallback/retry. Existing local Limits are larger; these limits are qualification restrictions, not shared capacity promises.

Pending history has exactly one proof/attempt-evidence record; the later resolved representation has exactly three (original plus FUTURE_FENCE and NO_EXECUTION), each containing full evidence and historical correlation and exact TARGET+RESOURCE coverage. Partial-key proofs, exclusions, extra proof growth, multi-attempt or arbitrary intermediate resolution are blocked in this profile; they require another qualified profile, never dropping evidence. Reservation is required before hypothetical handover for the two later complete records. Saturated reserve is measured below. Historical delivery/error/dispatch capture remains unchanged; flags derive from retained covered proof. No target claim is actually verified by these synthetic PROJECT_DESIGN records.

Ordinary Favorite refs, original bindings, typed arguments, deadline/epoch, all relevant captures and contracts remain exact. No recipes, numeric operations, URI/content selection, assets, seek windows, alternate route, live scheduling, whole-result reconstruction, or arbitrary reassociation. Same-owner rollback records retain original target/bindings and increasing previous/current generations; ownership-changing merges/rollback are excluded. Exclusion evidence must be empty. Title observations/preconditions use exact STRING or explicit absence. Pending observation request IDs correlate to the retained intent. No generic Record inference.

Encoding validates a candidate before fake PREPARE/bank/seal/handover. Count/text/identity/schema limits refuse before any storage change or simulated emission. A failed allocator update must remain blocked, not reissue a consumed pair. Successful refusal-pair persistence advances lifetime/ticket together; exhaustion refuses. Capacity refusal for maximal input emits zero commands. No implementation claims are made for mapping arbitrary live Store into this profile: production integration and its unsupported-case admission gate do not exist.

## Every persistent path: clause and live source trace

Prefixes below cover every leaf, optional, tagged branch and bounded list in FIELD_PATHS. Names after / are local semantic aliases, never a changed frozen type.

| Persistent path prefix | Frozen clause(s) | Actual current source/type | Preservation rule |
| --- | --- | --- | --- |
| format_version, required_features, common_model_version | 1,2 | model.hpp Version; proposed codec envelope | v1/features0 only; future/older format blocked, no silent migration |
| registry_id, allocators.*, deleted_ids.* | 2,10,12 | core.hpp Store.lifetime_counter/watermark/epoch_base; core.cpp allocate/expected_id | all ID namespaces + scope/non-reuse metadata; deleted records never identify live objects; counters fixed UInt64 |
| clock_epoch, ingress_watermark | 3,10,12,18 | Store.clock_epoch/ingress; MonoTime | retain original epoch for correlation; restart must retire scheduling, not replay |
| devices.* | 2,4,16 | model.hpp CommonDevice + Evidence | identity/gen/evidence retained; labels/profile/manufacturer are non-safety presentation, not persisted |
| targets.* | 2,4,15,17 | Target + SharedResource membership | original identity/capability/media generations, resources and ordering retained |
| bindings.* | 2,4,17 | Binding | identity/ownership/all generations/versions/priority/mapping evidence/opaque private refs retained; no secrets |
| resources.* | 12,17 | SharedResource, LockKey | membership, ordering and full evidence; historical effect keys independent of later membership |
| associations.* | 16 | canonical recorded transactions (no dedicated persistent transaction type in current Store) | same-owner original IDs/bindings/evidence/previous+new gens/rollback phase retained; wider cases blocked |
| catalogs.*, items.reference.*, items.private_token | 2,6,15 | CatalogRecord/CatalogSnapshot/CatalogItem/SelectionRef; token capture is proposed private extension | full Favorite ref and continuity, all generations, label/variant and opaque private token, no URL or credential |
| conflicts.*, participants.* except resync_observation | 8,9,18 | ConflictState/ConflictParticipant/FieldSnapshot | latched roster, revision and each ingress/start watermark exact; exclusion proof cases blocked |
| conflicts.participants[].resync_observation.* | 3,8,9,15 | StateObservation/FreshnessPolicy/ProvenanceHop/Sequence | all normalized observation fields/provenance/time/source metadata retained as HISTORICAL only |
| effects.request.* | 10,12,13 | CommandRequest/StepCapture/FieldPrecondition/RouteCapture | full closed typed immutable envelope; explicit optional seek/recipe absent and unsupported |
| effects.attempt.* | 11,12,13 | Attempt/Progress/Error/ErrorCause | complete original attempt correlation, history, evidence and resource capture; no recipe step |
| effects.execution_contract.*, retry_policy.*, semantic_variant | 6,10,12,17 | Record.contract/ExecutionContract/RetryPolicy; CapabilityDescriptor semantic_variant | full original guarantees and policy retained, no current-descriptor substitution |
| effects.affected_keys.* | 11,12,17 | EffectKey/LockKey | TARGET+actual RESOURCE; per-key independent no_past/no_future state checked against retained signals |
| effects.proof_history.* | 11,12,18 | AdapterEvidence + Effect.evidence_ids (codec retains full proof, beyond existing IDs) | full evidence/body/coverage/correlation; distinct identities; digest-only proof forbidden |
| effects.progress/complete/refused/uncertain_extent | 11,12 | Effect/Progress | narrow closed ambiguous history and later two-proof resolution; no invented emission/confirmation |
| effects.first_terminal_time/closure_error/invalidated/scheduling_closed | 11,12,13 | Record.result/stop_error/stopped and terminal retention rules | historical closure metadata; full old result is not recreated after retirement |

Source anchor: unchanged [A-002 snapshots](../A-REMOTE-002/INDEX.md), checked against A-003 full entry SHA inventory. Clause anchor: frozen COMMON_CONTROL_MODEL_V1.md SHA7a46f9fffe706476de458aac078d0af1c94844df339248d3f9f4b5cf033011d7. Private token/allocator/association/proof-history extensions are proposed projection data, not claims that current Store already stores them durably.

## Deliberately non-recovered runtime data and safety gate

AdapterRoute.adapter pointers/callbacks/queues/tasks never persist. Current capability schemas/numeric mappings/support, authorization/reachability/contact, selected fields/optimistic overlays/display data and credentials are not certified by historical records. Recovery returns current_observations=[] and authorization=UNKNOWN and scheduling=[] and RECOVERED_BLOCKED, not READY. Re-verify current identity/contracts/session/context and target fences before future work. Full active/queued/dedup results and windows cannot be imported into this closed-history profile; old epoch requests must become HISTORY_EXPIRED, never scheduling. These gates are represented by the fake recovery result only, NOT implemented in Core. Result/dedup purge cannot delete the retained independent effect/barrier/proof/conflict projection. Missing projection means GLOBAL_BLOCK; never fallback to an older bank without a trustworthy newer-intent indication.

The encoder checks structural constraints, several scope/correlation/proof invariants and exact roundtrip. It is not a target-proof verifier or a full production recovery/session allocator. That limitation is a production blocker, not omitted evidence promoted to PASS.

## Canonical representation and maximum-size proof

Little-endian fixed-width integers, one-byte closed enums/bool/tag, u16 byte lengths/list counts, fields in explicit schema order. UTF-8 is strict; Rational is reduced and denominator>0. Top frame is 16 bytes (magic/version/features/payload length/CRC32). Map input order is irrelevant; ordered arrays remain significant. No compression assumed.

run_qualification.py derives structural maximum recursively and deducts only enforced semantic-profile restrictions (title STRING, RESOURCE second key, correlated generated intent IDs max27 bytes, absent seek/recipe/step/rollback_of). The saturated resolved fixture reaches that derived upper bound exactly. Maximum pending uses the same saturated legal data with original single proof, leaving the two-proof reserve. Scalar primitive tests cover exact integers/rationals/enums independently; other operation schemas remain blocked.
