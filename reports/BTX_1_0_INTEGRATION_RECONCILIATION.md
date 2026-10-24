# D-011 / BTX 1.0 integration reconciliation

Status: **SOFTWARE VERIFIED / READY FOR HARDWARE PREPARATION / HARDWARE ACCEPTANCE PENDING**

## Frozen authority

- Approval head: `e5bec2d639ec6c99cd52aabaafa3e52582754105`.
- Specification: `references/RTCP_1_BLUETOOTH_EXTENSION_V1_PROPOSED.md`.
- Exact bytes: 18,318; SHA-256: `6391f46d1f789aa5468474dc6aa475324bff95cf1abca4dea716fb3016524db9`.
- Frozen behavior: exact first D-009 ID 3/4 exchange; authenticated second ID 3 probe; ID 12 negotiation or legacy ID 4 fallback; IDs 13/14 state; ID 15 commands; correlated result ID 8; 96-byte artist and 127-byte title; 512-byte plaintext transport ceiling; session/source/generation fencing; one request in flight and no automatic retry.

## Repository reconciliation

| Device | Base chain | Implementation | Current PR head | Status |
| --- | --- | --- | --- | --- |
| TUNER | D-009 PR #7 `79d247893095b9464583c3cfe0e612d7683871c9` → mDNS PR #8 `216f5a14d375652543d3f722141acbf526bee8c8` | `bc9c148a942732c890fcba6e6b15769bc4cd9067` | PR #9 `1ac32909f0fe1697f0a7301cd1d3c79956b1a92f` | OPEN / UNMERGED / software verified |
| REMOTE | A-REMOTE-014 discovery → D-009 PR #4 `271a6578737a5f314bb33cc1aefc2fc4986ad0d7` | `5b32cbbeb554cd8a4d49094a5bd7c4797fd0b403` | PR #5 `2200bc8df02262e076ecdbd3c9fd66eac4c5d3b3` | OPEN / UNMERGED / software verified / reconciled |

REMOTE reconciliation used a normal merge of current PR #4 into PR #5. Only additive changelog history conflicted; both D-009 and BTX histories were preserved. No executable file changed in the reconciliation commit, so the passing focused tests and production build were not repeated.

A-REMOTE-013 D-009 Round 5 remains **PARTIAL HARDWARE PASS**. Its verified hardware evidence remains valid as the baseline under BTX; cases previously marked untested remain untested.

## Candidates and rollback

| Item | Bytes | SHA-256 | Verification |
| --- | ---: | --- | --- |
| TUNER BTX candidate/readback | 2,072,960 | `67fbeb56082fffddb6104f5ed948395bc862262cf5bcb10602292b08cb3ad590` | exact private candidate and independent readback present |
| REMOTE BTX candidate/readback | 2,582,432 | `5d84f83b8e9e6f860e7cd807a270eeee697ed42dc361bbb1e1022f639dc4206b` | exact private candidate and independent readback present |
| TUNER D-009 rollback | 2,040,704 | `1e6c5968f539170656e833d023086c57986b1aa73a6c2fe982dee2b31b1ff1f6a` | exact candidate and hardware readback present |
| REMOTE D-009 Round 5 rollback | 2,578,352 | `6eb44ff4137d8c11f44dc5e0fed0a7061f77b172d4a38982e5219bbd7454e278` | exact hardware readback present |

Separate USB Stage 1 rollback copies were rehashed: TUNER full 4 MiB `4a980e0887fab052389c233429d9cdf398720e119f2b51141a4fcfb8aa5914f6`, TUNER application slot 3 MiB `3ce83b7a6f9e9132b34df5dd8168e6874932bb74618457584c8337967911a6c1`, REMOTE full 16 MiB `31fd537c4bf534b101e74ed582bf0aa909235686207da29ad61413f21688b43d`, and REMOTE factory application slot 8 MiB `a2cdad46d173856a051bcf143a148d730f4ce9d47a17446411c2475b2383efea`. Private paths, binaries and device identifiers are not published.

The current running firmware identity on either device is **UNKNOWN** in this read-only source/filesystem reconciliation. Existing installation evidence is historical and cannot substitute for a current hardware readback or embedded build identity.

## Compatibility and limits

- TUNER-first rollout preserves old-REMOTE operation: the first capability response remains exact D-009; old REMOTE never sends the second probe.
- New REMOTE against old TUNER receives legacy ID 4 on the second probe and keeps authenticated D-009 plus volume while disabling BTX.
- New/new enables BTX only for the authenticated session. Disconnect, sleep, restart or rollback clears extension authority.
- TUNER: 2,072,960-byte app, 89,904-byte static RAM, 1,072,768-byte slot headroom, 60-byte persistent BTX state.
- REMOTE: 2,582,432-byte app, 56,652-byte static RAM, 563,296-byte slot headroom, 232/320-byte persistent growth and 192/195-byte HOME snapshot growth.
- TUNER callback-derived A2DP audio state is contract-compliant source authority. Physical validation must confirm phone Play/Pause produces reliable authoritative transitions; if it does not, AVRCP play-status callback evaluation requires separate authorization.
- An accepted BTX command result proves authenticated TUNER admission and local AVRCP submission only. Phone/player-specific AVRCP support may vary and must be observed with the intended phone and representative player applications; the software evidence does not claim that every phone applies every command.

## Remaining hardware acceptance

No hardware operation occurred in this reconciliation. The exact gated procedure is in `handoffs/BTX_1_0_LATEST.md`. Mandatory evidence remains: current device identity and firmware identity, TUNER-first mixed-version compatibility, new/new negotiation, Bluetooth connect/reconnect and metadata lifecycle, Play/Pause/Previous/Next and refusals, radio ↔ Bluetooth stale clearing, volume preservation, sleep/wake and RTCP reconnect, MP3/A2DP/HTTP coexistence, runtime internal heap/minimum heap/largest block/allocation failures, exact-span readbacks and independent rollback of each device.

