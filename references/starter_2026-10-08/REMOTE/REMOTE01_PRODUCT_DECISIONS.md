# REMOTE//01 canonical product decision register

2026-10-05 - Today's Step2 owner-approved reconciliation. Authority: explicit owner request in attachment86e54181-6a73-4328-ab6e-ba3384067b6c/Pasted text.txt, sections A-I. This register supersedes conflicting current product classifications in older audits/proposals; it does not rewrite historical evidence or grant implementation/hardware acceptance.

Statuses: DECIDED; DESIGN REQUIRED; IMPLEMENTATION + HARDWARE VALIDATION REQUIRED; SUPERSEDED; EXCLUDED; UNKNOWN / NOT RECOVERED. Owner wording OPEN / DESIGN REQUIRED is normalized to DESIGN REQUIRED; EXCLUDED / DECIDED to EXCLUDED (explicit owner decision). Historical suggestions remain historical, not a seventh current status.

| Owner item | Status | Exact canonical scope / boundary |
| --- | --- | --- |
|1|**DECIDED**|REMOTE//01 and TUNER//01 are physically separate devices.|
|2|**DECIDED**|TUNER owns internet-radio streaming, decoding, playback and audio output; REMOTE does not locally decode/play internet radio.|
|3|**DECIDED**|REMOTE finds artwork for the active stream URL, retrieves/caches it and displays a thumbnail while that media/URL context is active; obsolete results cannot replace current artwork.|
|4|**DECIDED**|Dormant REMOTE codec/audio BSP is not used for internet-radio playback; it may remain excluded until cleanup and is hardware inventory only.|
|5|**DECIDED**|REMOTE is designed primarily for TUNER, retaining protocol-neutral model/adapter boundaries for Home Assistant and openHAB compatibility. Product positioning is not generic-first or TUNER-independent.|
|6|**DECIDED**|TUNER Native is primary/first native target. Home Assistant/openHAB are intended compatibility integrations. Matter/Smart-TV/IR retain historical/intended direction without priority over TUNER Native or support claims.|
|7|**DECIDED**|Home Assistant/openHAB are optional integrations, not mandatory hubs or the architectural center.|
|8|**EXCLUDED**|Zigbee is explicitly excluded by owner decision; not UNKNOWN / NOT RECOVERED.|
|9|**SUPERSEDED**|Local-versus-external playback selection gates and active REMOTE local-radio streaming/decoder/I2S/audio-output workstreams are outside current product scope. Historical comparisons retained only as superseded.|
|10|**DECIDED**|Use mDNS for TUNER discovery; manual IP/hostname fallback may remain. No service name/port/identity hints are approved by this decision.|
|11|**UNKNOWN / NOT RECOVERED**|Actual TUNER wire protocol not recovered/verified; existing Native API candidate remains unapproved/unfrozen.|
|12|**DESIGN REQUIRED**|Select transport after actual TUNER source/capabilities/protocol verification; do not freeze WebSocket + HTTPS.|
|13|**DECIDED**|User-accessible Network Settings/reprovisioning for router/network/location changes, showing current IP/status.|
|14|**DECIDED**|Wi-Fi credential reset and general/factory reset remain separate operations.|
|15|**DESIGN REQUIRED**|Define exact general/factory erase scope and retention policy.|
|16|**DECIDED**|Development/Mock UI is temporary; approved production UI replaces it.|
|17|**DESIGN REQUIRED**|Finalize production navigation/focus/settings/reset/media flows.|
|18|**DECIDED**|One rotary encoder plus three physical buttons.|
|19|**IMPLEMENTATION + HARDWARE VALIDATION REQUIRED**|Implement/verify GPIO mapping, encoder A/B, push presence/pin if used, button pins, active levels/pulls/electrical levels, detents/pulses and physical CW/CCW; invent no assignments.|
|20|**DESIGN REQUIRED**|Explicitly design/freeze encoder CW/CCW, push if present, three button meanings, screen/focus behavior, short/long presses if used and control-specific wake; do not claim actions were never approved.|
|21|**DECIDED**|Motion wakes only without control/playback intent; first asleep-display touch wakes only, subsequent touch operates; normal recovery cannot depend on inaccessible PWR.|
|22|**DECIDED**|Automatic system sleep remains inhibited while external-power state is not trustworthy.|
|23|**DECIDED**|Owner will add a divider from external 5V to an ESP32 GPIO/ADC input. Verify source pad/voltage physically; select GPIO after resource review and resistor values after voltage/resource verification. No values/pins invented. Detect external PRESENT/ABSENT only, not charging unless separately proven.|
|24|**DECIDED**|SD purpose: keep a firmware backup before flashing/updating.|
|25|**SUPERSEDED**|SD-purpose OWNER DECISION REQUIRED and UNKNOWN / NOT RECOVERED classifications superseded by decision24; do not carry them as current status.|
|26|**SUPERSEDED**|SD staging/SD OTA suggestions are not canonical SD purpose; retained historical proposals only, not required or implemented paths.|
|27|**IMPLEMENTATION + HARDWARE VALIDATION REQUIRED**|Verify routing/card detect/power; implement bounded mount/unmount/I/O/removal/error handling separately from decided purpose.|
|28|**DECIDED**|Persistence: favorites/recent stations -> TUNER; Wi-Fi credentials/settings, REMOTE UI settings, last associated TUNER and artwork cache -> REMOTE.|
|29|**DECIDED**|REMOTE does not persist station database/favorites; reads TUNER favorites for presentation/selection; TUNER executes playback.|
|30|**DECIDED**|Station/favorites persistence capacity/lifetime on REMOTE is not a product requirement. TUNER-side limits remain outside this repository unless verified target evidence is available.|
|31|**DESIGN REQUIRED**|Define survival/erasure for Wi-Fi reset, factory reset, UI settings, last associated TUNER, artwork cache and local service state. Ownership does not select reset scope.|
|32|**DECIDED**|REMOTE owns complete artwork lookup/discovery, retrieval/download, cache and display function.|
|33|**DECIDED**|Bind artwork to current URL/media context; discard late results from obsolete context.|
|34|**DESIGN REQUIRED**|Artwork lookup sources/mechanism, formats, dimensions/bytes, timeout, redirects/errors, decode policy, cache size/eviction/lifetime and absent-artwork fallback.|
|35|**DECIDED**|OTA required; accepted16MiB factory + otadata + ota_0 + ota_1 infrastructure remains unchanged.|
|36|**DECIDED**|OTA allowed from same local network without password authentication. Supersedes earlier authentication-required/LAN-insufficient OTA access requirement; no upload implementation authorized here. This does not change Wi-Fi provisioning security or TUNER control authentication.|
|37|**DECIDED**|Before flashing/updating, write a firmware backup to SD. Requirement is not currently implemented/validated; no claim earlier uploads created such a backup.|
|38|**DESIGN REQUIRED**|OTA image identity/compatibility, downgrade policy, interruption behavior, trial boot/health confirmation, rollback and relationship between factory/ota_0/ota_1/SD backup. Access policy does not select image trust/signature policy.|

## Frozen model versus product policy

Frozen CCM remains unchanged: context/asset safety, logical DEVICE_NATIVE versus REMOTE_RECIPE semantics, identity/session/authorization, evidence and durable command-history/barrier rules continue to apply to supported operations. Supporting logical favorite variants does not require this product to persist a REMOTE station/favorite database. Product chooses TUNER-owned station/favorite persistence; mandatory Core command-history persistence is a separate model concern, not station persistence. No direct frozen-CCM contradiction found. OTA access policy is outside CCM control-command authorization and does not weaken TUNER binding verification.

## Implementation and acceptance boundaries

Decisions are not implementation proof. Current SD backup, artwork pipeline, external5V divider sensing, integrated physical inputs and OTA writer/transfer/trial/rollback are not claimed implemented or owner-validated. No pin/resistor/image format/cache quota/erase-domain/protocol choice is invented. Same-LAN OTA access and image trust/compatibility are separate concerns; remaining trust/recovery design must follow the decided no-password access policy.

Today's Step1 remains CLOSED / OWNER HARDWARE VALIDATION PASS for reported running checks; Stage2B.2 closed for covered paths. Broader historical Stage1 remains OPEN for existing evidence gaps. Network Settings backend physical validation remains BLOCKED BY DESIGN / MISSING USER-ACCESSIBLE UI OR HARNESS, not FAIL; OPEN_SETUP/CANCEL/confirmed Wi-Fi reset not claimed owner-tested. WoM prior incident remains real/currently not reproduced/root cause unknown. No feature implementation/build/upload accompanies this reconciliation.

## Documentation verification / exact scope

Created this register; modified CHANGELOG.md plus CONTROL_ARCHITECTURE.md, REMOTE01_COMPLETION_ROADMAP.md, REMOTE01_RADIO_ARCHITECTURE_DECISION.md, REMOTE01_AUDIO_RADIO_AUDIT.md, REMOTE01_SD_AUDIT.md, REMOTE01_PHYSICAL_CONTROLS_PLAN.md, REMOTE01_OVERNIGHT_2_REPORT.md, REMOTE01_OVERNIGHT_EXECUTION_REPORT.md, TUNER_NATIVE_API_V1.md and STAGE_2B_LOCAL_OTA.md. Complete prior roadmap/radio/audio/architecture/API/OTA text remains byte-preserved under explicit historical/supersession overlays; overnight reports append-only; corrected SD/controls preserve exact replaced audit wording in historical quotations. CHANGELOG previous entries retained.

All38 owner items use only the six approved statuses; local Markdown-document links checked. SHA-256 scope comparison: all3982 other entry files (including source, tests, configuration, build artifacts and frozen CCM/reviews) unchanged;11 modified documents/one added/zero deleted. Documentation validation only, no compilation, tests, build or upload. Entry/final inventories retained in session TEMP; no new hardware acceptance claimed.
