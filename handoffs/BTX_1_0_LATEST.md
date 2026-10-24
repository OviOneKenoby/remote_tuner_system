# BTX 1.0 latest handoff

Status: **READY FOR HARDWARE PREPARATION / NO HARDWARE WRITE AUTHORIZED**

## Exact resumable state

- Frozen authority: proposal head `e5bec2d639ec6c99cd52aabaafa3e52582754105`; spec SHA-256 `6391f46d1f789aa5468474dc6aa475324bff95cf1abca4dea716fb3016524db9`.
- TUNER: PR #9 open/unmerged, head `1ac32909f0fe1697f0a7301cd1d3c79956b1a92f`, executable source `bc9c148a942732c890fcba6e6b15769bc4cd9067`, candidate 2,072,960 bytes / SHA-256 `67fbeb56082fffddb6104f5ed948395bc862262cf5bcb10602292b08cb3ad590`.
- REMOTE: PR #5 open/unmerged, reconciled head `2200bc8df02262e076ecdbd3c9fd66eac4c5d3b3`, executable source `5b32cbbeb554cd8a4d49094a5bd7c4797fd0b403`, candidate 2,582,432 bytes / SHA-256 `5d84f83b8e9e6f860e7cd807a270eeee697ed42dc361bbb1e1022f639dc4206b`.
- REMOTE base: current D-009 PR #4 head `271a6578737a5f314bb33cc1aefc2fc4986ad0d7`; reconciliation merge preserved all D-009 Round 5 fixes and evidence.
- Exact candidates, independent readbacks, D-009 rollback images and separate-USB Stage 1 backups are verified. Current running firmware identities remain UNKNOWN until hardware preflight.

## TUNER-first deployment gate

1. Obtain separate owner authorization for hardware access and the TUNER application-only write.
2. Identify TUNER from its ROM/chip interface, verify 4 MiB flash and installed partition table, then verify the candidate and all rollback hashes again. If the current app already matches the BTX candidate, skip the write.
3. Otherwise write only 2,072,960 bytes at `0x10000`; preserve bootloader, table, NVS, OTA metadata and pairing. Independently read back the exact span and require the candidate hash.
4. With the existing D-009 REMOTE, require authenticated identity, exact legacy first capability behavior, volume, radio D-009, MP3, A2DP and web-manager coexistence. Record internal free/minimum heap, largest internal block and allocation failures. Stop on regression.
5. Obtain separate owner authorization for the REMOTE application-only write. Identify ESP32-S3 and 16 MiB flash, reverify candidate/rollback, write only 2,582,432 bytes at `0x10000`, and require exact-span readback hash equality.
6. Validate new/new second-probe negotiation and BTX state. Exercise radio ↔ Bluetooth, phone connect/disconnect/reconnect, metadata variants and live changes, Play/Pause/Previous/Next, stale generation/refusal cases, volume, sleep/wake, reconnect and no stale replay.
7. Re-run MP3/A2DP/HTTP/RTCP coexistence and resource observations. Preserve raw private evidence; publish only sanitized results.

## Rollback

- TUNER application rollback: 2,040,704 bytes, SHA-256 `1e6c5968f539170656e833d023086c57986b1aa73a6c2fe982dee2b31b1ff1f6a`, application-only at `0x10000`, only under separate authorization, followed by exact-span readback.
- REMOTE application rollback: 2,578,352 bytes, SHA-256 `6eb44ff4137d8c11f44dc5e0fed0a7061f77b172d4a38982e5219bbd7454e278`, application-only at `0x10000`, only under separate authorization, followed by exact-span readback.
- Full-flash copies are emergency recovery evidence and must not be used as routine rollback. Never erase or overwrite NVS, pairing, credentials, partition tables or unrelated regions.

## Stop conditions

Stop before writing if device identity, flash size, partition bounds, candidate hash, rollback hash or independent storage evidence differs. Stop after any write/readback mismatch, boot failure, authentication regression, audio/network regression, unsafe resource result or unexpected reset. Do not retry, roll back, merge or release automatically.

Next action: owner review and separate authorization for the TUNER read-only preflight/application-only commissioning stage. TUNER playback-state authority remains a physical acceptance item; source changes are not justified without a reproducible callback-state failure.

Phone/player-specific AVRCP support is an explicit acceptance boundary: an accepted RTCP result proves TUNER submission, while authoritative callbacks and physical audio/metadata observation must prove the phone applied the command.
