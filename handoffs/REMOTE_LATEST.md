# REMOTE//01 handoff

## Metadata

- Handoff ID: REMOTE-A-REMOTE-011-STAGE5-HARDWARE-COMMISSIONING-PASS-20261016
- Updated (UTC): 2026-10-16
- Task ID: A-REMOTE-011
- Status: STAGE 5 HARDWARE COMMISSIONING PASS; VALIDATED ROLLBACK BASELINE
- Coordination branch: `remote/a-remote-011-kickoff-20261013`, PR #17
- Input head: `56979e3113ea81839d0ac6e60f71fa35b021f1ae`

## Result

A-REMOTE-011 Stage 5 hardware commissioning is PASS for the verified scope. The owner confirmed correct EC11 detection and direction, correct individual one-step volume changes, five rapid down detents changing authoritative TUNER volume from 95% to 90%, and rapid reversal of three down plus two up changing 95% to 94%. RTCP command submission and authoritative volume synchronization passed, no persistent `IN_FLIGHT` latch remained, and one sleep/wake cycle produced no stale command replay.

The direction-reversal result is owner-verified. The cumulative diagnostics observed during commissioning also contain additional rotations, so they are retained as supporting operational evidence rather than claimed as an isolated five-detent counter delta.

Validated REMOTE rollback baseline: application offset `0x10000`; size 2,523,936 bytes; SHA-256 `38b43de02bf1ef69b85678f0a67451836cb0a24e3bf1876283933b3185ed4d5d`; exact flash readback PASS; OTA headroom 621,792 bytes. Preserve this private application and existing rollback evidence. No firmware/source/build/flash operation occurred during final acceptance.

Remaining open items: PR #17 remains open and unmerged pending owner disposition; no later A-REMOTE-011 milestone has been started. Previously documented out-of-scope items, including unassigned additional button actions and the separate intermittent motion-wake initialization observation, remain unchanged.

## Installation evidence

The expected REMOTE ESP32-S3 identity, accepted candidate and retained 16 MiB rollback backup were verified. The 2,523,936-byte application was written once at `0x10000`; exact readback matched SHA-256 `38b43de02bf1ef69b85678f0a67451836cb0a24e3bf1876283933b3185ed4d5d`. No other flash range was written.

After boot, the read-only diagnostics service reported stored Wi-Fi/configuration, valid voltage telemetry, RTCP stage complete, an authoritative volume, `volume.set` available and no volume command in flight. No encoder rotation, key press or RTCP control command was performed. The next step is the already documented controlled five-detent and reversal retest; hardware fast-rotation remains pending until owner-observed confirmation.

## Candidate implementation evidence

The accumulator candidate was installed and single-detent control remained correct, but hardware fast rotation still failed. The decisive snapshot recorded 19 detents/intents, seven local acceptances, final admission `VOLUME_SET_UNAVAILABLE`, no outstanding command, and unchanged session/capability revision. Source-level reproduction identified the missing test condition: `development::Session::snapshot()` cleared `volume_set` whenever `pending()` was true. Because `Channel::volume_admission()` requires that flag, every detent arriving during the active RTCP command was rejected before it could update the desired target. The prior unit tests supplied capability-ready snapshots directly and therefore did not exercise the Session wrapper's pending-state projection.

The minimum correction leaves authoritative `volume.set` capability visible while a command is pending. Playback actions remain disabled during that interval. Safety remains in the Channel: rapid detents only update one bounded desired-volume byte, one command remains in flight, and the next step waits for authoritative target observation. Definite failure, uncertainty, disconnect, session/capability change and sleep retain the prior safe behavior. The existing real-mode `dispatches` status field now reports actual RTCP client-accepted volume submissions instead of the historical constant zero; it remains a bounded counter and does not imply remote execution.

Focused reproduction and accumulator tests passed: 5/5 with 132 assertions; HOME integration 41/41 with 3,560 assertions. Full native regression passed: Core 69/69 (2,425 assertions), profile 6/6, hardening 26/26 (278,368 assertions), ingress 18/18 (22,189 assertions), power 19/19 (19,236 assertions), network 17/17, network-sleep 9/9, external-power 11/11, portal 15/15, diagnostics 9/9, physical-input 19/19, both WoM modes 7/7, both stack modes 7/7, OTA preflight 8/8, and all remaining boundary/publication suites. One `remote01` production build passed. Private candidate: 2,523,936 bytes; SHA-256 `38b43de02bf1ef69b85678f0a67451836cb0a24e3bf1876283933b3185ed4d5d`; 621,792 bytes OTA headroom; 47,228/327,680 bytes static RAM.

No hardware access or flash occurred. For the separately authorized retest, verify and install only this exact application at `0x10000`, verify exact readback, boot and wait for RTCP READY. Capture `encoder_detents`, `volume_intents`, `volume_intents_accepted`, `volume_admission`, `dispatches`, `volume_value`, `volume_in_flight`, session/revision and event cursor. From authoritative 95%, apply five fast down detents and wait for settling. Require all three input counters to increase by five, actual RTCP submissions eventually to increase by five, authoritative volume 90%, no outstanding operation and no new Core refusal. Then test three down plus two up for net 94%, followed by one sleep/wake or reconnect with no stale replay. Stop at the first mismatch; do not retry commands automatically.

## Prior accumulator candidate

Physical testing of the installed prior repair confirmed correct single-detent control and no persistent latch. Rapid detents still lost steps because `Channel::volume_admission()` rejected every detent while `volume_outstanding` was true. The hardware evidence isolated the loss before Core/RTCP: all 34 detents produced intents, but only 25 were locally accepted, with `IN_FLIGHT` as the observed rejection. The mock-only real-mode dispatch counter was not used.

The private correction uses one fixed desired-volume byte plus a validity flag; memory remains bounded regardless of rotation rate. Rapid detents adjust that clamped target. Only one one-step command exists at a time, and the next command is emitted only after a fresh authoritative observation reaches the previous target. Rapid reversal adjusts the desired target. A matching definite no-execution failure cancels pending changes; confirmed commands wait for authoritative state; uncertain delivery remains blocked; disconnect, session/capability change and sleep invalidation cancel pending changes. No timeout, automatic retry, optimistic UI update or weakened CCM precondition was introduced.

Tests passed: accumulator/admission/lifecycle 5/5 with 132 assertions; encoder routing 5/5 with 26 assertions; actual HOME/Core/Facade path 40/40 with 3,548 assertions; RTCP rational/admission 2/2 with 221 assertions. One production `remote01` build passed. Private candidate: 2,523,904 bytes; SHA-256 `89ada9b2ff6f339398e3cb0470395dfbc37637bfca97d788e74190258db414de`; 621,824 bytes of 3 MiB OTA headroom; 47,228/327,680 bytes static RAM.

No hardware access or flash occurred. Commission only after separate owner authorization: verify the exact candidate and rollback image; write/read back only the application at `0x10000`; confirm boot, RTCP READY and authoritative volume; from a verified 95% start apply five fast down detents and require 90%, five accepted intents and no outstanding operation after settling; test three down plus two up as net one down; then perform one normal sleep/wake or reconnect and require no stale command replay. Stop on the first mismatch and do not retry control commands automatically.

## Prior pipeline repair

Hardware diagnostics prove that EC11 transitions, detents and intents reach the HOME channel. They also prove that one locally accepted volume intent remained in flight and blocked later detents. Source inspection established the responsible lifecycle defect: `Channel::request()` latched the intent, while the runtime discarded both the immediate `Facade::handle()` result and later request lifecycle; only connection/session/capability changes or an exact target observation could clear it. Existing `CORE_REFUSED` events are consistent with this path, although the bounded historical event ring cannot identify the original token. The real-mode `dispatches` value is intentionally always zero and was not used.

The private repair tracks the exact volume-intent token. Immediate Core rejection and terminal Core outcomes proven to have executed nothing release only that matching token. Stale or unrelated outcomes cannot clear it. Confirmed commands remain protected until authoritative volume reaches the target; uncertain delivery remains blocked until authoritative state or session invalidation, preventing blind retry. Both command and observation percentages use canonical reduced rationals, and volume/playback observation submissions are independent. CCM validation, authentication, freshness, bounds, ordering and single-in-flight behavior remain strict.

Focused verification passed: volume admission/lifecycle 3/3 (42 assertions), RTCP rational/admission 2/2 (221 assertions), and the actual HOME/Core/Facade path 40/40 (3,548 assertions). One production `remote01` build passed. Private candidate: 2,523,504 bytes; SHA-256 `4d084c074d74f7ba366f868d52eb45cbe3fb4a517980842c80fc4405efded57d`; 622,224 bytes of 3 MiB OTA headroom; 47,228/327,680 bytes static RAM.

No hardware access, flash, TUNER change, pairing/NVS/partition mutation or live volume command occurred. The physical result remains unverified. Separate authorization is required to install this exact application, confirm RTCP synchronization, then test one detent in each direction and a bounded two-detent volume-down sequence at 100%, including authoritative feedback and one sleep/reconnect cycle with no stale replay.

## Prior installation result

The accepted 2,522,912-byte REMOTE application was installed once at `0x10000` after device, rollback and partition preflight. Exact readback matched SHA-256 `7382e69ce03544b5282cd4d38cece0a01fd8a74b8e739823676dbf3fac5165b9`. Normal boot retained stored Wi-Fi/configuration, valid voltage telemetry and the existing UI service.

Read-only evidence confirms authenticated RTCP identity, completed capability negotiation and continuing validated encrypted records. The installed freshness-policy correction is active, but CCM still reports no authoritative volume or `volume.set` capability. The first failing admission condition is exact: `RtcpDevice` constructs `volume.level` as the unreduced rational `{percent,100}`, while Core requires a normalized reduced rational. Because the snapshot handler combines the volume and playback publishes with short-circuit `&&`, the rejected volume also prevents submission of `playback.state`. The HOME volume indicator cannot display an admitted authoritative value.

No encoder rotation, key press, control command, TUNER change, source/build operation, pairing/NVS/partition mutation or PR merge occurred. The minimum next action is a separately authorized adapter correction that reduces the volume rational before publication, with one focused admission regression and one REMOTE production build. Core strictness and TUNER behavior should remain unchanged.

## Historical context

The diagnostic application installation and exact readback remain PASS. Both devices remain reachable at their expected LAN addresses with working Wi-Fi. One owner-authorized bounded TCP probe established a connection to the exact provisioned TUNER RTCP port in 35 ms and closed without sending data. The TUNER listener and TCP path are therefore available.

REMOTE snapshots continued to show failed reconnect lifecycle advancement with no authenticated connection, authoritative volume, `volume.set` capability, in-flight request, invalid/refused result or dispatch. The retained original commissioning capsules have valid structure and match each other on endpoint port, pairing identifier and PSK without reading or exposing the secret values. Stage 4 had previously proved these same provisioned identities could authenticate.

The first proven failure boundary is now after TCP establishment and before REMOTE completes its authenticated-connect transition. In the implemented client, that transition requires receipt and validation of the TUNER server hello and successful transmission of the client finish. Capability and encrypted identity negotiation occur later and were not reached. Existing status and retained logs do not expose whether the server hello was absent/truncated or its proof validation failed, so neither pairing corruption nor a specific cryptographic defect is demonstrated.

## Scope guard

Only existing automatic client behavior, read-only LAN/status evidence and one zero-payload TCP establishment probe were used. No repeated probe, RTCP payload, manual reconnect loop, encoder rotation, control command, source/build/flash change, NVS/pairing/configuration change, secret publication or PR merge occurred.

## Next owner action

Keep both devices online and do not rotate the encoder. The smallest supported next step is bounded, secret-free REMOTE instrumentation recording only: TCP connected, client hello completely sent, server hello byte count received, server-hello framing valid, server proof valid, client finish completely sent, and first identity response accepted. Counters plus one last-failure enum are sufficient. REMOTE is the minimum device because its current authenticated-connect transition is the missing boundary; TUNER instrumentation is unnecessary unless REMOTE proves that it sent a valid client finish. This requires a separately authorized source change, build and application-only installation. Pairing reset or regeneration is not justified.

## Evidence

- `reports/A-REMOTE-011_STAGE5_DIAGNOSTIC_INSTALL_RESULT.md`
- `references/device_evidence/remote/A-REMOTE-011/STAGE5_DIAGNOSTIC_INSTALL_RESULT.json`
- Candidate build: `reports/A-REMOTE-011_STAGE5_DIAGNOSTIC_ARRAY_FIX.md`

## Read-only RTCP reconnection diagnosis

- REMOTE application and diagnostics: reachable.
- REMOTE stored Wi-Fi/network state: connected, zero reported network or allocation errors.
- Privately provisioned TUNER endpoint: not reachable and absent from current neighbor discovery.
- Existing automatic reconnect activity: observed through advancing capability-revision and lifecycle counters.
- RTCP stage reached: TCP endpoint connection not established; mutual authentication, identity negotiation, ready capabilities and fresh snapshots not reached.
- Classification: current TUNER/network endpoint outage or address availability issue; no REMOTE software defect demonstrated.

## Read-only retry result

- REMOTE and provisioned TUNER endpoint: both reachable at expected LAN addresses.
- Both devices: Wi-Fi connected.
- REMOTE automatic reconnect lifecycle: continuing.
- RTCP result: still disconnected; no authoritative volume, `volume.set` capability, in-flight request or dispatch.
- Exact boundary: after IP reachability and before authenticated capability/snapshot completion.
- Diagnostic limit: current status does not expose TCP connect, server hello, client finish or encrypted identity substates; no exact substage can be claimed.
- Earlier endpoint-unreachable classification: temporary and superseded for current state.

## RTCP transport diagnosis

- Configured endpoint and retained capsule association: structurally consistent; matching secret fields verified privately without disclosure.
- Single bounded TCP probe: established in 35 ms; zero payload bytes sent; no repeat.
- TUNER RTCP listener and TCP route: available.
- REMOTE built-in reconnects: continue to fail before the authenticated-connect event.
- First proven failure boundary: server-hello/authentication transition after TCP establishment and before capability or encrypted identity negotiation.
- Not distinguishable from current evidence: missing/truncated server hello versus failed server-proof validation versus client-finish send failure.
- Minimum instrumentation: REMOTE-only bounded stage counters and last-failure enum for TCP connect, client-hello send, server-hello receive/framing/proof, client-finish send and identity response. No key, nonce, proof, identifier or payload logging.

## Bounded handshake diagnostics implementation stop

The requested private REMOTE diagnostics are implemented with fixed storage: stable stage/failure enums, a non-secret platform error code, saturating counters and server-hello byte count. They cover TCP establishment, completed client hello, server-hello receive/framing/proof, completed client finish and encrypted identity request/response acceptance. No endpoint, identifier, key, nonce, proof, raw message or payload is retained, and RTCP behavior is unchanged.

The first focused host-test compilation exited 1 without compiler output and produced no executable. The first-failure stop applied; no retry and no production build occurred. Firmware size, SHA-256, OTA headroom and static RAM remain unavailable. See `reports/A-REMOTE-011_STAGE5_RTCP_HANDSHAKE_DIAGNOSTICS_STOP.md`.

The previously proposed single retry has now been consumed and failed identically. Any toolchain-process diagnosis or execution on a different verified host requires a new owner decision. The production build and installation remain blocked.

## Authorized single compilation retry result

The compiler executable, working directory, source, include root, diagnostic header and writable output location were verified before the unchanged retry. The single authorized compilation again exited 1, emitted zero stdout and zero stderr, and produced no executable. No focused test or production build ran. The result demonstrates a repeatable immediate host compiler-process failure for this command but supplies no compiler diagnostic that attributes it to source. No additional retry, source change or hardware action occurred. The implementation remains unverified and installation remains blocked.

## Compiler environment resolution and focused-test result

The owner demonstrated that the missing MSYS2 UCRT64 runtime directory in the Windows process PATH caused the silent compiler exits. Prepending that directory only for the test process resolved the host failure. The focused RTCP diagnostic model then compiled and passed 6/6 assertions.

The next affected status-schema compilation exposed the first source-level blocker: the expanded Core snapshot makes `diagnostics::Snapshots` 1,120 bytes, exceeding the existing 1,024-byte static limit. The mandatory stop applied before any source correction or production build. The smallest next decision is whether to authorize a bounded representation change that retains all requested diagnostics within the existing snapshot/storage budget, followed by the failed schema check and one production build. Installation remains separately gated.

## Snapshot representation correction and production-build stop

The authorized minimum correction restores the existing 40-element Core values array and stores all requested RTCP handshake evidence in a fixed 16-byte member with ten saturating counters. `diagnostics::Snapshots` is exactly 1,024 bytes. The representation adds no allocation and leaves locking, API behavior and RTCP behavior unchanged.

The diagnostics schema passed 9/9 cases with 9,086 assertions, and the RTCP diagnostic model passed 6/6 assertions under the corrected process PATH. The single production build then stopped because the containing `diagnostics::Storage` is 8,208 bytes, exceeding its separate existing 8,192-byte guard by 16 bytes. No correction or second build occurred; firmware size, SHA-256, OTA headroom and final static RAM are unavailable.

The authorized 16-byte storage correction and single production build are now complete; the historical stop above remains evidence only. Installation remains separately gated.

## Storage correction and final build result

The overflow originated exactly from 1,024-byte `Snapshots`, 4,112-byte `Ring` and the 3,072-byte response buffer; no additional padding was present. Reducing only the response buffer by 16 bytes makes `diagnostics::Storage` exactly 8,192 bytes. Complete status serialization remains verified within the 3,056-byte buffer. Both existing size guards, fixed allocation, locking, security and RTCP semantics are preserved.

The directly affected schema/layout suite passed 9/9 cases with 9,087 assertions. The single production build passed. Private firmware: 2,522,560 bytes, SHA-256 `ac5e259eb8c57029e897b0106d44851d085b7d29ebc7d7bf827089dfadaf1a4d`; OTA headroom 623,168 bytes; static RAM 47,212 bytes. No hardware operation occurred. Separate owner authorization is required before application-only installation and runtime handshake diagnosis.

## Diagnostic installation stop

The accepted candidate and retained 16 MiB rollback backup reverified. Windows enumerated the expected Espressif native USB interface and reported it healthy, but the first read-only esptool identity operation failed while opening/configuring the port with Windows device error 31. The operation stopped before ROM identity, erase, write or readback. Zero flash bytes changed, and no boot or RTCP diagnostic observation occurred.

The minimum next action is for the owner to close any serial monitor or reconnect REMOTE, then separately request a retry. No automatic retry is authorized.

## Diagnostic installation retry and first proven RTCP failure

The expected REMOTE ESP32-S3 identity, 16 MiB flash and retained rollback backup were verified. The accepted application was written once at `0x10000`. An exact 2,522,560-byte readback matched SHA-256 `ac5e259eb8c57029e897b0106d44851d085b7d29ebc7d7bf827089dfadaf1a4d`.

After normal boot, read-only status showed stored Wi-Fi connected, the UI service available, valid battery/external-power telemetry and IMU ready. TUNER was reachable. Across two snapshots, RTCP attempts and successful TCP-connect counters advanced together, but completed client-hello remained zero; server-hello bytes and all later handshake counters remained zero. The stable diagnostic result was stage `tcp_connected`, failure `send`, platform error 119 (`EINPROGRESS`). No authenticated session, fresh volume or `volume.set` capability was established.

Source correlation identifies the first demonstrated cause: the nonblocking client checks `SO_ERROR` immediately and treats zero as completed connection without first waiting for socket writability. It then attempts the client-hello send while the connection is still in progress. This is a REMOTE connection-completion state defect before authentication; it does not demonstrate pairing corruption or a TUNER listener failure.

The minimum corrective action is to gate successful nonblocking connection completion on writable readiness and then confirm `SO_ERROR == 0`, preserving existing timeouts and reconnect policy. That source correction, build and installation require separate owner authorization. No source change, TUNER change, pairing/NVS/partition operation, encoder rotation, control command or PR merge occurred in this step.

## Nonblocking TCP completion correction

The private REMOTE client now polls the connecting socket for writability without blocking, keeps the existing three-second connection deadline, and reads `SO_ERROR` only after readiness. Pending and interrupted checks remain pending; timeout follows the existing diagnostic/cleanup path; socket and option failures remain explicit. Client-hello construction and transmission cannot begin until readiness plus `SO_ERROR == 0` confirm connection completion. RTCP messages, cryptography, authentication, retry timing and allocation behavior are unchanged.

The narrowly scoped readiness suite passed 9/9 cases. The single production build passed. Private artifact: 2,522,848 bytes, SHA-256 `cdda9773981a3d5dd5008d1380d50f6738a4796fc6a12430f4b3521b666b08f7`; 622,880 bytes of 3 MiB OTA headroom; 47,212 bytes static RAM. No hardware access or persistent operation occurred. Application-only installation and runtime confirmation require separate owner authorization.

## Corrected RTCP firmware installation stop

The accepted private application and retained rollback backup reverified. Windows enumerated the expected Espressif USB interface and no serial-monitor process was identified, but the required esptool ROM identity check failed while opening/configuring the port with Windows device error 31. The operation stopped before device identity, erase, application write or readback. Zero flash bytes changed, and no runtime RTCP observation was possible. Owner action is to restore the USB serial connection and separately authorize a retry.

## Corrected RTCP firmware installation retry

The verified REMOTE ESP32-S3 and 16 MiB flash identity matched the retained rollback evidence. The accepted application was written once at `0x10000`; exact 2,522,848-byte readback matched SHA-256 `cdda9773981a3d5dd5008d1380d50f6738a4796fc6a12430f4b3521b666b08f7`. Normal boot exposed stored Wi-Fi, the existing UI service and valid voltage telemetry.

The nonblocking-connect correction worked: diagnostics recorded TCP ready, client hello sent, complete 56-byte server hello received, framing valid, server proof valid, client finish sent and encrypted identity request sent. No identity response was received or accepted. The session then disconnected and the existing automatic reconnect policy continued. Capability negotiation and fresh `volume.level`/`volume.set` availability were therefore not reached.

The first demonstrated remaining failure boundary is after the authenticated client finish and encrypted identity request, before receipt of the TUNER identity response. No control command, encoder rotation, source/build change, TUNER change, pairing/NVS/partition change or PR merge occurred. Further diagnosis or encoder testing requires separate owner authorization.

## Missing identity-response source diagnosis

REMOTE's `identity_request_sent` counter advances only after `lwip_send` accepts every byte of the encrypted record into the local TCP stack. It does not prove peer receipt or processing. Existing REMOTE evidence proves zero identity-response header bytes reached its parser, but the subsequent reconnect resets the displayed last-failure category; the retained counters cannot distinguish prior timeout, EOF or peer close. TUNER currently exposes no RTCP receive/authentication/close diagnostics.

Static comparison found the implementations aligned on the previously working Stage 4 path: client-finish transcript, directional HKDF labels, session identifier, record type/version, counter 1, c2s nonce, 28-byte authenticated header, four-byte identity request and identity response format. TUNER should validate the record header/session/counter, authenticate AES-GCM, accept the identity request, build the response and write it before advancing its transmit counter. No framing, sequence or cryptographic mismatch was demonstrated.

The first proven boundary is therefore: REMOTE locally submitted the complete encrypted identity request, while no identity-response header arrived before disconnect/reconnect. The exact cause remains unknown. Plausible locations are request delivery, TUNER header/session/counter validation, GCM authentication, request dispatch, response creation or response write; these remain hypotheses.

The smallest next observation is bounded, secret-free TUNER-side counters and one close-reason code for: client finish accepted, record header/full record received, header/session/counter valid, GCM valid, identity request accepted, response generated and complete response write. REMOTE changes, pairing reset and protocol probes are not justified. This observation requires separate authorization for TUNER instrumentation, build and application-only installation.

## Minimal TUNER diagnostics implementation build stop

The private TUNER server now has a 60-byte fixed diagnostic structure with saturating counters for client-finish acceptance; record header/full receipt; framing, session and counter validation; GCM acceptance; identity dispatch, response generation and complete write; plus timeout, EOF, transport error, close count and last close reason. The existing `/api/diagnostics` endpoint exposes only these counters/codes. No secret, identifier, nonce, proof or packet content is stored or logged, and protocol behavior is unchanged.

The focused model passed 4/4. The single build itself succeeded with a 2,031,568-byte image, SHA-256 `a058ef716e9d866d8e2165bbe8364d8badd7fec53452fe673bb906f0f46a08da`, 1,114,160 bytes of nominal 3 MiB slot headroom and 85,968 bytes reported static RAM. However, it used the default `esp32-dev` environment; the accepted installed/Stage 4 production baseline uses `esp32-lwip-psram`. The artifact is therefore rejected and must not be installed or treated as production verification. The first-unexpected-result stop prevented a second build.

The minimum next action is one separately authorized build of the unchanged diagnostic source with `esp32-lwip-psram`. No hardware or persistent operation occurred.

## TUNER diagnostics production build correction

PlatformIO configuration and the accepted Phase 3 baseline confirm `esp32-lwip-psram` as the TUNER production environment. It extends the established UART-probe environment for board `esp32dev` (Espressif ESP32 Dev Module) and enables the required PSRAM/lwIP allocation path. The unchanged private source completed the single authorized build successfully.

The production firmware is 2,036,400 bytes with SHA-256 `f193863f6d2966cc0797b9bdd2144971fb7b4bfc5bb9b1b4c07ff4840cf4a21c`. PlatformIO reports flash usage of 2,029,825/3,145,728 bytes (64.5%) and static RAM usage of 87,464/327,680 bytes (26.7%). Binary-length headroom in the 3 MiB application slot is 1,109,328 bytes. The already-passing focused model remains 4/4 PASS, and the bounded diagnostic storage remains exactly 60 bytes; tests were not repeated because their inputs did not change.

The earlier `esp32-dev` artifact remains rejected. No source/configuration change, hardware access, flash operation, pairing/NVS/partition mutation or control command occurred. Installing this private diagnostic firmware requires separate owner authorization.

## TUNER diagnostic firmware commissioning

Mandatory preflight identified the expected TUNER ESP32 through its physical CH340 interface, reverified the accepted private candidate and complete rollback evidence, confirmed the installed production application against its accepted hash, and decoded the verified table with `app0` at `0x10000` and size 3 MiB. The 2,036,400-byte diagnostic application was written once at `0x10000` using 921600-baud esptool communication. Exact readback matched SHA-256 `f193863f6d2966cc0797b9bdd2144971fb7b4bfc5bb9b1b4c07ff4840cf4a21c`.

TUNER booted with retained Wi-Fi, its audio service and RTCP listener available. Its bounded diagnostics recorded successful client-finish acceptance, complete encrypted-record receipt, framing/session/counter validation, GCM authentication, identity dispatch, identity-response generation and complete response writes. Timeout, EOF, transport-error and session-close counters remained zero. REMOTE diagnostics concurrently recorded identity-response receipt and acceptance with no RTCP failure or platform error.

No failure exists in the instrumented TUNER identity path. The remaining demonstrated boundary is later: REMOTE is connected and accepts identity, but still lacks a fresh authoritative volume and `volume.set` capability. The evidence does not identify its post-identity cause. No source/build change, flash retry, pairing/NVS/partition operation, encoder action or control command occurred. Any corrective investigation requires separate owner authorization.

## Post-identity capability and volume synchronization diagnosis

The expected sequence is identity request/response, capability request/response, initial snapshot request/response, then periodic snapshots while READY. Current bounded evidence proves that identity acceptance advances the REMOTE client, the capability exchange completes, the client reaches its complete/READY diagnostic stage, and TUNER continues receiving, validating and answering post-identity encrypted records. TUNER recorded no timeout, EOF, transport error or close; REMOTE remained connected with no RTCP failure.

The first failing transition is local REMOTE snapshot admission. The installed field descriptors are created through `MockAdapter::readable` with a 5,000 ms freshness bound and source-clock contract `bounded synthetic acquisition`. `RtcpDevice` submits live RTCP observations with a 2,000 ms bound and source-clock contract `same authenticated request/reply sample`. Core admission requires the observation freshness policy to equal the registered capability policy exactly, so it rejects every otherwise valid snapshot before selecting `volume.level` or `playback.state`. Diagnostics consequently show connected/READY negotiation but `volume_known=0`; the facade intentionally keeps `volume_set=0` until an authoritative volume is selected.

This is a rejected-observation defect, not a missing capability or snapshot message. The same descriptor/observation mismatch exists in the Stage 4 source path; the retained Stage 4 evidence established authenticated wire exchange but did not expose these later Core-admission fields, so it does not demonstrate successful admission against this mismatch.

The smallest corrective action is to register the two RTCP field capabilities with the exact live RTCP freshness policy already emitted by `RtcpDevice` (2,000 ms, verified sequence, matching source-clock contract), leaving CCM, RTCP framing and TUNER unchanged. That source correction, focused admission test and REMOTE build require separate owner authorization.

## RTCP capability freshness-policy correction

The private REMOTE source now defines one fixed RTCP freshness policy and uses it for both registration and observation of `volume.level` and `playback.state`: 2,000 ms, verified sequence, and source-clock contract `same authenticated request/reply sample`. No Core admission rule was relaxed, and no unrelated capability, protocol, cryptographic, timeout or reconnect behavior changed.

Changed private files: `components/control_home/include/control_home/rtcp_device.hpp`, `components/control_home/rtcp_device.cpp`, and `tests/control/rtcp_freshness_tests.cpp`. The focused regression passed 1/1 case with 6 assertions, demonstrating admission of the matching authenticated policy and rejection of the former mismatch. The single production `remote01` build passed. Private firmware: 2,522,912 bytes, SHA-256 `7382e69ce03544b5282cd4d38cece0a01fd8a74b8e739823676dbf3fac5165b9`; 622,816 bytes of 3 MiB OTA headroom; static RAM 47,212/327,680 bytes (14.4%).

No hardware access, flash operation, TUNER change, pairing/NVS/partition mutation, encoder action or control command occurred. Application-only installation and read-only synchronization verification require separate owner authorization.
