# A-REMOTE-009: 64KiB layout and USB/ROM recovery preparation
- Owner: REMOTE//01; authorized PM/executor for preparation publication
- State: ASSIGNED â€” PREPARATION IN PROGRESS; hardware execution BLOCKED pending explicit approval
- Coordination input commit: e6fa6f4911eb6bcd342d1db9600ad66f134636ab
- Objective: Produce a verified partition-only candidate and one safe, unexecuted owner backup/recovery/rollback protocol suitable for later hobby/public-beta hardware validation.
- Baseline: Protected private Git-less REMOTE source, project12_LVGL_Test/version1; source commit UNKNOWN. Read originals; create a disposable private build copy, preserving production source and installed tools. Installed A006/A007 image identity is historical evidence, not proof of current source/runtime equivalence.
- Required references: [Owner authorization](../references/A009_PREPARATION_OWNER_AUTHORIZATION_2026-10-12.md); accepted A006 layout/artifact evidence; A007 physical16MiB/table/factory/erased-region evidence; A008 final owner acceptance; templates/HANDOFF_TEMPLATE.md; prompts/CODEX_TASK_FOOTER.md.
- Dependencies: A006/A007 accepted evidence and D00864KiB layout approval; A008 DONE / OWNER ACCEPTED. CCM1.1.0 frozen. No backend/API implementation dependency is authorized.
- Allowed scope: Disposable private candidate adds remote_ctl,data,nvs,0xE20000,0x10000 only; local binary generation, entry-byte/MD5/bounds/alignment/overlap checks, current effective-config/source inspection, one serial clean build with at most one bounded clean retry for recognized Ryzen ICE; sanitized coordination task/report/hash/table evidence; unexecuted Windows USB/ROM owner protocol.
- Excluded scope: Hardware access, protocol execution, persistent hardware operations, production-code/tool mutation, TUNER changes, private source/bundle publication, durable backend/common API/MQTT/SmartThings/UI, A010, CCM/A008 reopening and unrelated industrial qualification.
- Shared-contract guard: CCM1.1.0 OWNER APPROVED/FROZEN and historical CCM1.0.0 unchanged; Native UNAPPROVED/UNFROZEN/NOT IMPLEMENTED; O01â€“O17/common gate OPEN/NOT PASSED. A009 is layout/recovery preparation only.
- Acceptance criteria: All six existing32-byte entries byte-identical to installed accepted baseline; append exactly one64KiB NVS entry; verify4KiB data/64KiB app alignment,16MiB bounds/no overlap and both3MiB OTA slots unchanged. Hash CSV/BIN and candidate firmware/artifacts when generated; record tools/config/build result and OTA headroom. Protocol requires exact device/COM confirmation, current physical size/security/table checks, private complete16MiB verified backup before writing, minimal table-only write, reboot checks and backup-based ROM rollback with explicit STOPs. Keep PR OPEN/unmerged and hardware NOT RUN.
- Verification: Host-only generation, parsing/entry-byte comparison, clean -j1 build, source/tool preservation hashes, sanitized-publication checks and fresh remote verification. Build evidence and historical A007 hardware evidence remain distinct; no new hardware validation.
- Stop/report conditions: Baseline mismatch, moved/reduced partition, wrong bounds/alignment, security/encryption restriction, concrete functional/data-loss/security/bricking risk, secrets in proposed public material, non-ICE build failure or second recognized compiler failure. No automatic flash, erase, upload, NVS or recovery operation; explicit owner approval required before the first persistent hardware operation.
- Required outputs: Assignment/owner record, layout/build report, safe generated table/patch/hashes, single unexecuted hardware protocol, private-copy device changelog, coordination CHANGELOG, byte-exact archived/latest complete REMOTE handoff and new OPEN/unmerged PR.
- PM assignment evidence: Owner instruction2026-10-12 and [published authorization](../references/A009_PREPARATION_OWNER_AUTHORIZATION_2026-10-12.md); assignment commit reported after remote publication.

## Mandatory execution footer

Coordination checkout: current isolated coordination checkout (private absolute path intentionally omitted from public material).
Device: REMOTE.
Read AGENTS.md, README.md, PROJECT_SYNC.md, API_STATUS.md, DECISION_REGISTER.md and both latest handoffs. Record the coordination input commit. Confirm the real firmware baseline before editing. Missing evidence must be reported, not guessed.

Execute only the assigned task. CCM1.0.0 historical approval remains frozen; current CCM1.1.0 is owner-approved/frozen. Native is unapproved/unfrozen/not implemented. Stop dependent implementation and submit a proposal if shared-contract change is needed.

At completion or blockage, update the device changelog in the disposable private review copy and coordination CHANGELOG. Archive the prior complete REMOTE latest handoff using README naming rules; replace latest using every heading/field of the exact handoff template. Separate inspected facts, planned work, local artifacts/build evidence and historical physical evidence. Publish no private source, credentials, bundles or hardware dump. Reread current coordination state before publication and preserve concurrent changes. Report final coordination commit separately; if publication fails, report UNPUBLISHED without claiming DONE.

## Preparation outcome — 2026-10-12T18:35:41.124995+00:00
PASS — HOST LAYOUT/RECOVERY PREPARATION; HARDWARE NOT RUN. [Report](../reports/A-REMOTE-009_PREPARATION.md); [unexecuted protocol](../protocols/A-REMOTE-009_USB_ROM_RECOVERY.md). Hardware authorization remains pending; no hardware/protocol execution or A010 start. Assignment commit `b55176d8f9a2a18f175c6eae027a62e235f63d1f`.
