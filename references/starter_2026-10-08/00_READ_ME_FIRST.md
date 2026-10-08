# READ ME FIRST — REMOTE//01 + TUNER//01 Project Manager starter pack

Date: 2026-10-08

This ZIP is a bootstrap package for a separate Project Manager / System Architect chat.
Its job is coordination, not firmware development.

## Current project structure

- REMOTE//01 and TUNER//01 are separate firmware projects and separate development chats.
- TUNER is the authoritative media/audio device.
- REMOTE is the direct LAN client/controller.
- Home Assistant and openHAB are optional additional clients, never mandatory gateways.
- REMOTE + TUNER must work directly on the LAN without HA/openHAB/MQTT/Matter/cloud.

## Highest-authority current handoff

Start with:

`SHARED/TUNER_REQUIREMENTS_FROM_REMOTE.md`

This is the current REMOTE-side handoff contract produced after the separate TUNER source audit.
It explicitly keeps Native API v1 UNAPPROVED / UNFROZEN / NOT IMPLEMENTED.
Section 22 is the TUNER implementation acceptance checklist.
Section 24 is the current open-decision register O01-O17.

## Verified TUNER baseline

Repository: OviOneKenoby/ESP32-WROVER-Internet-radio
Branch: main
Commit: 371cdebce7ba2648ea71636d5bdb5d738b42e680
Firmware: 1.1.0

The files in `TUNER/` are the source-backed audit/architecture/capability/implementation-plan records for that exact baseline.

## Important provenance warning about two REMOTE reference files

The available mounted copies of the following files predate later documentation status transitions:

- `REMOTE/COMMON_CONTROL_MODEL_V1_PRE_FREEZE_REFERENCE.md`
- `REMOTE/TUNER_NATIVE_API_V1_PRE_AUDIT_CANDIDATE.md`

Do NOT use their header/status wording as the current project status.

Later project records establish:
- Common Control Model (CCM) 1.0.0 is OWNER APPROVED / FROZEN.
- The freeze introduced no normative semantic redesign; it was the approved progression from candidate.4.
- TUNER Native API v1 remains UNAPPROVED / UNFROZEN / NOT IMPLEMENTED.
- A separate TUNER v1.1.0 audit now exists and supersedes the Native API candidate's old claim that TUNER implementation evidence was unavailable.

These two files are included only because they still contain useful semantic/design reference content. The Project Manager must not silently promote their stale status text.

`REMOTE/REMOTE_CHANGELOG_AVAILABLE_2026-10-06.md` is also an available snapshot, not the 2026-10-07 documentation milestone generated locally after the TUNER handoff.

## Current common phase

PHASE A:
- REMOTE: Native contract reconciliation / CCM mapping / minimum v1 subset.
- TUNER: correctness + coherent control/state ownership foundation.

Do not freeze the Native API yet.

## Coordination rule

No shared interface decision may be changed unilaterally by either device chat.
Shared decisions are coordinated by the Project Manager and then handed back as separate tasks to REMOTE and TUNER.

Use `PROJECT_MANAGER_BOOTSTRAP_PROMPT.md` as the first prompt in the new Project Manager chat.
