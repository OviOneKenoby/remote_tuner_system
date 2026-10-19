# A-REMOTE-013 D-009 hardware validation protocol

**UNEXECUTED.** Every flash or persistent operation requires separate owner authorization. Use the accepted 921600-baud esptool preference with 460800 fallback and exact-span SHA-256 verification.

## 1. TUNER-first commissioning

1. Verify physical identity, 4 MiB flash, application partition capacity, candidate size/hash, and local plus external rollback backups.
2. Flash only the authorized TUNER application at `0x10000`; independently read back the exact span and require its hash.
3. Confirm normal boot, Wi-Fi, stored configuration, MP3 and existing RTCP listener.
4. With the currently installed old REMOTE, verify identity/capabilities, volume observation/set, playback observation and reconnect. Confirm it ignores new capability bits and sends no IDs 9–11.
5. Verify TUNER local play/pause and fixed-list previous/next remain unchanged. Verify discovered-mode Next still performs only its local documented Favorite gesture and is never invoked by RTCP.
6. During MP3 and A2DP with web manager active, record free/minimum internal heap, largest internal block, allocation failures, resets, HTTP and RTCP responsiveness. D-009 controls remain unavailable in A2DP.

Stop for owner review before REMOTE installation.

## 2. REMOTE commissioning

1. Verify physical identity, 16 MiB flash, candidate size/hash, application capacity, and local plus external rollback backups.
2. Flash only the authorized REMOTE application at `0x10000`; independently read back the exact span and require its hash.
3. Confirm UI, Wi-Fi, stored configuration, voltage telemetry, sleep/wake, pairing and existing volume behavior.
4. Confirm authenticated READY, capability revision 2, fresh playback/station/metadata and zero pending command.
5. Verify the existing HOME station line and now-playing line; confirm the generated brightness page, artwork placeholder, carousel geometry and other screens are unchanged.

## 3. Joint functional cases

- Play from paused radio: one request, accepted result, fresh PLAYING.
- Pause from playing radio: one request, accepted result, fresh PAUSED.
- Previous and next in fixed list: one guarded traversal each, correct station/generation, old metadata cleared before new metadata.
- Empty/stale/discovered/Bluetooth context: control disabled or one explicit refusal, no Favorite mutation and no AVRCP command.
- No-metadata station: station remains visible; now-playing shows neutral state.
- Long valid title: safe codepoint-boundary truncation and no corruption.
- Malformed UTF-8: metadata unavailable; no raw invalid text reaches LVGL.
- Frequent metadata changes: latest authoritative text, bounded memory and responsive audio/network/UI.
- Disconnect during/after send: no automatic retry, pending result fenced, stale text cleared; reconnect restores authoritative state.
- SYSTEM_SLEEP/wake: no replay; state and metadata resynchronize.
- Local TUNER station/state change: REMOTE follows authority without optimistic success.

## 4. Rollback

Rollback is application-only, one device at a time, using the already verified private artifact for that device and exact-span readback. Roll back REMOTE first if only the new client regresses. Roll back TUNER if the server/audio path regresses. Do not erase or restore NVS, pairing, partitions or full flash without separate authorization. Mixed-version behavior must remain volume-compatible throughout.

## 5. Stop conditions

Stop on identity/hash/readback mismatch, boot failure, lost settings/pairing, protocol/security failure, unintended Favorite/AVRCP action, stale metadata association, command replay, audio/web regression, allocation failure, reset, or material A2DP heap regression. Do not retry writes or widen scope automatically.
