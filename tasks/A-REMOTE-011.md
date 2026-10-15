# A-REMOTE-011: Common REMOTE-TUNER API integration kickoff
- Owner: REMOTE//01 with coordinated TUNER//01 changes
- State: IN PROGRESS - STAGE 5 BUILD PASS / MOTION-WAKE CURRENT BOOT IMU INITIALIZATION FAILURE CONFIRMED
- Coordination input commit: `8e93c702940d49583f3fdd58046503ae0b8f7354`
- Objective: implement the frozen RTCP/1 transport and first CCM 1.1.0 REMOTE-TUNER integration slice, verify both builds and stop before hardware commissioning.
- Baseline: coordination main `8e93c702940d49583f3fdd58046503ae0b8f7354`; Phase 2 coordination input `1e11e979dbcd4d95a50cbf8ed87400ce854256b3`; TUNER v1.1.11 `5fb92c95d228d744d1182ae3956e850c5be2f277`; accepted A-010 private REMOTE source.
- Required references: `references/CCM_1_1_0.md`; `docs/TUNER_NATIVE_API_V1.md` in the private REMOTE source; current coordination handoffs; `reports/A-REMOTE-010_CLOSURE.md`; `reports/A-REMOTE-011_KICKOFF.md`; `reports/A-REMOTE-011_PHASE1_RECONCILIATION_TRANSPORT.md`.
- Dependencies: A-REMOTE-010 DONE / OWNER ACCEPTED; CCM 1.1.0 OWNER APPROVED / FROZEN; RTCP/1 Phase 2 profile specified; Phase 3 source implementation is complete; Phase 4 procedure is prepared; Stage 1 and both Stage 2 installations passed; the private Stage 3A helper is implemented and build verified; separate owner approval is required before credential generation, helper flashing or pairing writes.
- Allowed scope: backed-up active-workspace promotion; private REMOTE and public TUNER RTCP/1 integration; first CCM functional slice; focused host tests and clean builds; English sanitized coordination publication.
- Excluded scope: operational PSK generation, device access, flashing, hardware changes, AAC/AAC+ work, stations, playback commands, UI redesign, MQTT, SmartThings, CCM semantic changes, private-source/binary/credential publication, STL/manual publication, A-REMOTE-012.
- Shared-contract guard: CCM 1.1.0 semantics and the frozen RTCP/1 Phase 2 profile remain unchanged; the implementation adds only the approved first functional slice.
- Acceptance criteria: active private source is reversibly promoted; exact RTCP/1 and first CCM slice compile on both devices; focused tests and clean builds pass; memory/flash deltas are recorded; coordination PR remains open and unmerged; hardware is not run.
- Verification: Phase 3 evidence retained. Stage 2A and 2B passed. Stage 3A implemented private compile-time helpers matching both production readers; 16/16 focused host tests and commissioning plus normal builds passed. One-shot and explicit partial-recovery gates preserve unrelated TUNER NVS and REMOTE A-010 generation history. No credentials were generated and pairing remains absent.
- Stop/report conditions: baseline mismatch; missing A-010 source state; unresolved security/transport treated as if approved; any request to publish private material; any firmware or hardware operation.
- Required outputs: reversible commissioning protocol, sanitized evidence checklist, archived prior handoff, current handoff, changelog/status entries and updated open coordination PR.
- PM assignment evidence: owner instructions dated 2026-10-13 in the active session; Phase 3 authorizes backed-up promotion, private/public source implementation and build verification, stopping before hardware operations.

## Stage 4 completed 2026-10-14

PASS at the approved practical hobby/public-beta level. Both accepted production applications were restored at `0x10000` and independently read back with their accepted hashes. Pairing and ordinary configuration remained present, both devices booted normally, and the owner confirmed normal UI. The paired devices established an authenticated RTCP/1 session, accepted the exact CCM 1.1.0 identity/capability sequence, and continued receiving fresh bounded `volume.level` and `playback.state` snapshots. Zero RTCP control commands were dispatched. See the [completion report](../reports/A-REMOTE-011_STAGE4_COMPLETE.md) and [sanitized result](../references/device_evidence/remote/A-REMOTE-011/STAGE4_RESULT.json). The earlier stopped report remains historical evidence. A single controlled `volume.set` remains separately gated and unexecuted; PR #17 remains open and unmerged.

## Stage 5 stopped before transmission 2026-10-14

A live authenticated session passed the read-only precondition check, but the production REMOTE has no wired volume intent or `volume.set` request-construction path. The CCM/RTCP adapter implements validated correlated delivery; the production facade exposes only previous/toggle/next, and the serial development hook refuses commands in RTCP mode. Zero commands were transmitted and no state was mutated. See the [stop report](../reports/A-REMOTE-011_STAGE5_CONTROL_STOP.md) and [sanitized result](../references/device_evidence/remote/A-REMOTE-011/STAGE5_STOP_RESULT.json). A narrow source implementation and build require a separate owner decision before Stage 5 can resume.

## Stage 5 encoder routing blocked before source edit 2026-10-14

The active and preserved private sources contain only a host-tested quadrature model. They contain no production encoder sampler, GPIO identity, event consumer, LVGL encoder device or context router. The implementation therefore stopped before editing rather than guessing hardware or changing navigation semantics. No tests/builds were run because no valid source change existed; no hardware/control action occurred. See the [routing blocker report](../reports/A-REMOTE-011_STAGE5_ENCODER_ROUTING_BLOCKER.md) and [sanitized result](../references/device_evidence/remote/A-REMOTE-011/STAGE5_ENCODER_ROUTING_BLOCKER.json).

## Stage 5 owner pin assignment rejected after hardware verification 2026-10-14

The owner identified the encoder as GPIO4 CLK / GPIO5 DT and reserved GPIO1. The official Waveshare V2 schematic labels IO4 `BAT_ADC`, and the active private firmware continuously uses ADC1 channel 3 with a compile-time GPIO4 mapping for main-battery sensing. GPIO1 separately remains ADC1 channel 0 for external-power sensing. The requested pair therefore fails the mandatory conflict check. A transient private implementation passed focused tests and built, but is rejected and non-deployable; every transient source edit was reverted. No hardware or control operation occurred. See the [GPIO conflict report](../reports/A-REMOTE-011_STAGE5_ENCODER_GPIO_CONFLICT.md) and [sanitized result](../references/device_evidence/remote/A-REMOTE-011/STAGE5_ENCODER_GPIO_CONFLICT.json).

## Stage 5 GPIO resolution proposal 2026-10-14

Official V2 schematic/interface evidence and the active production source identify GPIO2/J6-3 and GPIO5/J6-6 as the only accessible J6 pair without onboard loads, production claims or ESP32-S3 strapping roles. J6-9 is the proposed ground common. The complete map rejects GPIO0/GPIO3 strapping pins and occupied GPIO1/GPIO4, and preserves every LCD, touch, power, USB, UART, I2C, SD and audio net. No source, build, test or hardware action occurred. Owner approval of the exact wiring and physical J6 orientation is required before implementation. See the [GPIO map](../docs/REMOTE_GPIO_MAP.md), [investigation report](../reports/A-REMOTE-011_STAGE5_GPIO_RESOLUTION.md) and [sanitized result](../references/device_evidence/remote/A-REMOTE-011/STAGE5_GPIO_RESOLUTION.json).

## Stage 5 approved encoder implementation stopped at build 2026-10-14

The owner approved GPIO2/J6-3, GPIO5/J6-6 and J6-9 GND. The bounded private implementation passed 5/5 encoder/admission cases and the existing quadrature suite passed 19/19 cases. The one clean production build then stopped at its first failure: `user_app` could not resolve the existing shared `physical_input/model.hpp` header because its component include path does not expose the private root include directory. No correction or second build was attempted. No firmware artifact, hardware action or live command exists. See the [stop report](../reports/A-REMOTE-011_STAGE5_ENCODER_IMPLEMENTATION_STOP.md) and [sanitized result](../references/device_evidence/remote/A-REMOTE-011/STAGE5_ENCODER_IMPLEMENTATION_STOP.json).

## Stage 5 include-path correction result 2026-10-14

The private shared include tree was registered as a header-only ESP-IDF component and added to `user_app` private requirements. Exactly one production build was run and retained the original `fatal error: physical_input/model.hpp: No such file or directory` diagnostic. No distinct build error appeared; no additional correction, build or test was run. No firmware artifact or hardware operation exists. See the [result report](../reports/A-REMOTE-011_STAGE5_INCLUDE_PATH_RESULT.md) and [sanitized evidence](../references/device_evidence/remote/A-REMOTE-011/STAGE5_INCLUDE_PATH_RESULT.json).

## Stage 5 component discovery resolved 2026-10-14

Generated metadata proved that the failed build tree predated the new header-only component: it omitted both `physical_input` and the shared include directory from `user_app`. Preserving and displacing only that generated tree forced fresh discovery. The one authorized production build passed; the private 2,518,496-byte application has SHA-256 `58d09a4d7b39a287d80b48270b5236986657f27fb716692b77ff4af3e573cab7` and 627,232 bytes of 3 MiB OTA headroom. Previously passing tests were not repeated because no relevant source changed. No hardware or live command occurred. See the [resolution report](../reports/A-REMOTE-011_STAGE5_COMPONENT_DISCOVERY_RESOLVED.md) and [sanitized evidence](../references/device_evidence/remote/A-REMOTE-011/STAGE5_COMPONENT_DISCOVERY_RESULT.json).

## Motion-wake regression diagnosis 2026-10-15

No A-011 source regression was demonstrated: the active IMU, expander, GPIO8 wake and power path is byte-identical to preserved A-010/A-011 baselines and the core files from the earlier owner motion-wake PASS snapshot. Wake-on-motion remains enabled, but initialization runs only once per boot and an initialization or status-read failure disables the motion path until reboot. Earlier evidence records the same `IMU_WOM=0` failed-lift state without a proven root cause. Current runtime evidence is required. No source, build or hardware action occurred. See the [diagnosis](../reports/A-REMOTE-011_MOTION_WAKE_DIAGNOSIS.md) and [sanitized evidence](../references/device_evidence/remote/A-REMOTE-011/MOTION_WAKE_DIAGNOSIS.json).

## Motion-wake runtime result 2026-10-15

One read-only snapshot from the verified running REMOTE reported display idle, `IMU=0`, zero motion events, four wakes, zero runtime bus errors and last sleep cause zero. The mandatory stop applied before movement, so no lift or snapshot B occurred. The combination of IMU not ready and zero runtime bus errors classifies the current failure at boot wake-on-motion initialization; the exact failed QMI stage requires a separately authorized passive UART capture during a normal reboot. See the [runtime result](../reports/A-REMOTE-011_MOTION_WAKE_RUNTIME_RESULT.md) and [sanitized evidence](../references/device_evidence/remote/A-REMOTE-011/MOTION_WAKE_RUNTIME_RESULT.json).
