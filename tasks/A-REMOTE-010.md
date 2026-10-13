# A-REMOTE-010: minimal private persistence backend

- Owner: REMOTE//01; authorized executor/publisher.
- State: HOST PHASE OWNER ACCEPTED; STAGE 3 READ-ONLY UART VALIDATION PASS; READY FOR SEPARATELY AUTHORIZED INITIALIZATION.
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

## Diagnostic continuation published 2026-10-13T06:43:09.576743+00:00

Owner accepted the host phase and authorized diagnostic design/implementation/review/build only. Result: PASS — diagnostic candidate implemented, 28/28 focused tests PASS, ESP-IDF adapter review PASS, clean candidate build PASS, partitions exact A-009, and zero hardware operations. See [report](../reports/A-REMOTE-010_DIAGNOSTIC_CANDIDATE.md), [evidence](../references/device_evidence/remote/A-REMOTE-010/DIAGNOSTIC_RESULT.json), and [complete unexecuted protocol](../protocols/A-REMOTE-010_HARDWARE_VALIDATION.md). PR #16 remains OPEN/unmerged; A-REMOTE-011 is NOT STARTED. Exact hardware approval remains required.

## Stage 1 read-only preflight published 2026-10-13T07:00:27Z

PASS — the owner-authorized read-only preflight bound the newly enumerated device to COM3, confirmed the expected ESP32-S3 revision and 16 MiB physical flash, matched the installed seven-entry table to accepted A-009, verified all 65,536 `remote_ctl` bytes remain `0xFF`, and matched the installed factory-image bytes to the accepted pre-A010 identity. See the [report](../reports/A-REMOTE-010_STAGE1_READ_ONLY_PREFLIGHT.md) and [sanitized result](../references/device_evidence/remote/A-REMOTE-010/STAGE1_READ_ONLY_RESULT.json). No firmware flash, write, erase, NVS initialization or diagnostic command occurred. Stage 2 and all later mutation stages remain blocked pending explicit owner approval; A-REMOTE-011 is NOT STARTED.
## Stage 2 diagnostic firmware validation published 2026-10-13T07:19:42Z

PASS — the exact 2,503,936-byte diagnostic candidate was written once at `0x10000`, independently read back byte-identical at SHA-256 `308181d4144494734fe8fae360938f74b9f886fb4c41bff0cba9b89427e4d248`, and booted once with the exact A010 identity and `persistence_on_boot=0`. Automated boot review found no panic, watchdog, partition error or boot loop; the owner confirmed normal UI and retained observable configuration. The complete `remote_ctl` region remained 65,536 bytes of `0xFF`, exact Stage 1. See the [report](../reports/A-REMOTE-010_STAGE2_DIAGNOSTIC_FLASH.md) and [sanitized result](../references/device_evidence/remote/A-REMOTE-010/STAGE2_RESULT.json). No diagnostic command, NVS initialization, commit or erase occurred. Stage 3 and all later stages remain unexecuted; A-REMOTE-011 is NOT STARTED.
## Stage 3 read-only UART validation published 2026-10-13T07:28:53Z

PASS — exactly `!A010 INFO` and `!A010 STATUS` were sent once each. Both were accepted and returned the exact `remote_ctl` data/NVS identity at `0xE20000`/`0x10000`, erased state, schema 1, generation/next 0, no incomplete transaction, zero entry counts and `payload_logged=0`, with no unexpected error. See the [report](../reports/A-REMOTE-010_STAGE3_READ_ONLY_UART.md) and [sanitized result](../references/device_evidence/remote/A-REMOTE-010/STAGE3_RESULT.json). No source-code or firmware change and no mutating command occurred. The partition is ready for separately authorized initialization; Stage 4 and A-REMOTE-011 remain NOT STARTED.
