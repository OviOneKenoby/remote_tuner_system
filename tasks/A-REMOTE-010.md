# A-REMOTE-010: minimal private persistence backend

- Owner: REMOTE//01; authorized executor/publisher.
- State: IMPLEMENTED / HOST VERIFIED / READY FOR OWNER REVIEW; hardware NOT RUN / NOT AUTHORIZED.
- Coordination input: 3ed3ff49f8ff6ba548a8b3b23020ad6a32c4566f.
- Objective: smallest reliable versioned persistence backend for installed64KiB remote_ctl, sufficient as a generic storage primitive for later common-API state; API not implemented.
- References: [Owner authority](../references/A010_PRIVATE_IMPLEMENTATION_OWNER_AUTHORIZATION_2026-10-12.md); accepted A009 physical layout/recovery files, CCM1.1.0 section12.1; exact handoff/footer templates.
- Scope: private source implementation, focused tests of actual implementation and NVS adapter, bounded clean serial build; sanitized results and unexecuted hardware-validation protocol. Existing source/configuration changes preserved; no private source publication.
- Storage model: small generic/versioned envelope; exact record/payload/count/lifetime limits documented. Strict persistent sequence, no uncommitted-generation reuse, explicit durable ordering and authority publication. Incomplete/corrupt/stale/unknown/ambiguous state must fail closed, never silently select older authority. Recovery emits zero commands; test witness outside persistent domain.
- Required tests: erased initialization, first/successor commit, interruptions before root and final commit, corrupt records/root, duplicate generation, capacity refusal, restart/recovery, replay/nonmonotonic rejection; coherent whole-domain rollback recorded OUTSIDE V1 THREAT MODEL. Bounded host fault cases, not industrial exploration.
- Adapter requirements: label-only selection validated against data/nvs0xE20000/0x10000, no default NVS use/migration, safe full/no-free-pages/version error refusal without erase; explicit initialization only, no boot-time writes or payload/secret logging.
- Verification: clean -j1 build (one bounded retry only for recognized Ryzen compiler-process ICE), table identical to installed A009, artifact hashes/size/OTA headroom and selected component verification, source/credential-publication checks. No hardware access or write.
- Hardware protocol: retained A009 backup verification, exact reviewed artifacts and owner approval before first hardware write; controlled non-secret test records, reboot/recovery/UI/configuration checks, bounded STOP/rollback; NOT EXECUTED.
- Guards: CCM frozen, Native unapproved, O01–O17/common gate OPEN; A008/A009 DONE/OWNER ACCEPTED. No TUNER/common API/MQTT/SmartThings/UI/A011; no automatic merge or hardware execution.
- Acceptance: private implementation and focused host evidence/build result reviewable in a new OPEN/unmerged PR; hardware behavior remains NOT RUN. Concrete data-loss/security/bricking risk must be resolved or reported, never hidden as PASS.

## Mandatory execution footer

# Mandatory Codex task footer

Append this text to each scoped device prompt, filling the device and coordination path:

```text
Coordination checkout: <absolute-path>
Device: <REMOTE or TUNER>
Read AGENTS.md, README.md, PROJECT_SYNC.md, API_STATUS.md, DECISION_REGISTER.md and both latest handoffs. Record the coordination input commit. Confirm the real firmware baseline before editing. Missing evidence must be reported, not guessed.

Execute only the assigned task. CCM 1.0.0 is OWNER APPROVED/FROZEN. TUNER Native API v1 is UNAPPROVED/UNFROZEN/NOT IMPLEMENTED unless a later explicit owner-approved decision with evidence supersedes that status. Do not make unilateral shared-contract changes. Stop dependent implementation and submit a proposal if the task requires one.

At completion or blockage, update the device changelog and coordination CHANGELOG.md. Archive the prior handoffs/<DEVICE>_LATEST.md under archive/<device>/ using the naming rule in README.md. Replace the latest file with the exact templates/HANDOFF_TEMPLATE.md structure, filled completely: milestone, baseline, changes, verification, remaining unknowns, shared-contract impact, blockers, PM decision required, recommended next task, commit and hardware status, plus metadata.

Separate inspected facts, planned work, implemented work, build evidence and physical hardware evidence. Include exact procedures, results and evidence references. Do not mark the common gate passed or a contract approved. Publish the handoff with the firmware commit and report the final coordination publication commit separately. Reread current coordination state before publication and resolve concurrent changes without overwriting them. If access/publication is unavailable, provide the complete handoff and report it as UNPUBLISHED.
```

## Result published 2026-10-13T03:35:07.084328+00:00

PASS — private implementation / host verified / clean build; hardware not run. See [report](../reports/A-REMOTE-010_PRIVATE_BACKEND.md), [evidence](../references/device_evidence/remote/A-REMOTE-010/RESULT.json), and [unexecuted protocol](../protocols/A-REMOTE-010_HARDWARE_VALIDATION.md). PR #16 remains OPEN/unmerged. Owner acceptance and a reviewed diagnostic activation plus exact hardware-write approval are required before physical exercise. A-REMOTE-011 is NOT STARTED.
