# REMOTE//01 handoff

## Metadata
- Handoff ID: REMOTE-A-REMOTE-011-PHASE2-20261013
- Updated (UTC): 2026-10-13
- Task ID: A-REMOTE-011
- Status: PHASE 2 PASS — NETWORK INTEGRATION NOT STARTED
- Prepared by: authorized executor / coordination publisher
- Coordination input: PR #17 Phase 1 head `203de66f585416903eb9385ee01f7dcbd7db4d15`

## Milestone
Reconcile a disposable private REMOTE source copy to the accepted A-010 baseline, verify it, and freeze the exact bounded authenticated TCP record profile. Achieved without changing the named active workspace or either device firmware.

## Baseline
- Coordination branch: `remote/a-remote-011-kickoff-20261013`, PR #17
- Coordination main baseline: `8e93c702940d49583f3fdd58046503ae0b8f7354`
- REMOTE source baseline: owner-private active tree plus preserved accepted A-010 tree; no private content published
- TUNER baseline: v1.1.11/main `5fb92c95d228d744d1182ae3956e850c5be2f277`
- Contract: CCM 1.1.0 OWNER APPROVED / FROZEN; RTCP/1 is a transport binding only

## Changes
Created a disposable private reconciliation copy, published the Phase 2 result, exact RTCP/1 specification, executable non-secret vectors, focused transport tests, sanitized result JSON, changelog/task updates and this handoff. Corrected the obsolete Phase 1 ESP-NOW sleep sentence to TCP session invalidation/reconnect behavior.

No TUNER source, active REMOTE source, firmware on hardware, partition, operational credential or CCM semantic was changed.

## Verification
| Check | Result |
| --- | --- |
| Private source reconciliation | PASS: 1,715 accepted and 1,715 reconciled non-generated files; zero path/hash differences |
| A-010 backend tests | 14/14 PASS, strict C++20 warnings |
| A-010 diagnostic tests | 14/14 PASS, strict C++20 warnings |
| REMOTE clean production build | PASS, serial `-j1`, 533.92 s |
| Production diagnostics | DISABLED: definition and diagnostic identity/mutation strings absent |
| Static RAM / firmware / OTA headroom | 47,084 / 2,496,320 / 649,408 bytes |
| Partition binary | exact accepted A-009 SHA-256 `a144343580dbdadace66fccc5969d7557de3d4c4f15a61e76db205cc26348184` |
| RTCP/1 reference tests | 14/14 PASS |
| Hardware | NOT ACCESSED |

## RTCP/1 decision
One persistent TCP connection; private random 32-byte per-pair PSK; fresh 16-byte nonces and mutual HMAC-SHA-256 proofs; RFC 5869 directional AES-128-GCM keys and nonce prefixes; authenticated 28-byte header; 64-bit exact-next counter; 512-byte plaintext/556-byte wire maximum; one in-flight command; no automatic retry; fail closed and invalidate on disconnect/sleep/error; fresh handshake and full CCM resynchronization after reconnect.

## Resource budget and risk
TUNER uses two fixed 556-byte buffers, at most 512 bytes session/parser state and an initial 1 KiB crypto-context allowance, with no new task. Prefer PSRAM for wire buffers. Incremental flash planning ceiling is 64 KiB. Actual compile/link and runtime measurements remain required because TUNER internal heap is already tight during Wi-Fi + A2DP + web-manager coexistence.

## Remaining work / decision
Owner approval is required before promoting the reconciled private files into an implementation workspace and beginning the narrow network integration on TUNER and REMOTE. The approved first slice remains identity/version, capabilities, read-only `volume.level`, read-only `playback.state`, `volume.set` and reconnect resynchronization.

Operational PSK creation/provisioning, network integration, hardware access/flashing, station/playback commands, MQTT, SmartThings, AAC work and UI changes remain outside this phase. PR #17 stays open and unmerged.

## Evidence
- `reports/A-REMOTE-011_PHASE2_RECONCILIATION_PROTOCOL.md`
- `references/A_REMOTE_011_AUTHENTICATED_TCP_V1.md`
- `references/device_evidence/remote/A-REMOTE-011/PHASE2_RESULT.json`
- `tools/qualification/a_remote_011_transport/`
- Previous handoff preserved at `archive/remote/2026-10-13T160850Z_A-REMOTE-011_REMOTE-A-REMOTE-011-PHASE1-20261013T154500Z.md`
