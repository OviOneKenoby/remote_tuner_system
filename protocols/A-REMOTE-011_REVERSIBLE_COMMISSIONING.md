# A-REMOTE-011 reversible two-device commissioning protocol

## Status and authority boundary

**PREPARED — NOT EXECUTED.** This protocol targets practical hobby/public-beta assurance for the accepted Phase 3 candidates. It does not authorize device access, flashing, pairing, persistent mutation, or a control command. Every stage requires the stated owner authorization. Stop before Stage 1 until the owner authorizes read-only access to both devices.

The frozen CCM 1.1.0 and RTCP/1 specifications remain authoritative. This procedure does not alter their semantics.

## Fixed software identities and flash boundaries

| Device | Source identity | Candidate | Candidate SHA-256 | Exact candidate write range | Partition containing range |
| --- | --- | ---: | --- | --- | --- |
| REMOTE//01 | private Phase 3 source | 2,515,584 bytes (`0x266280`) | `ceae9f64329c5409fdfe92e5ac5394885010abf1cf66ac24a5ab7fcc35f11647` | `0x10000–0x27627F` | unchanged 8 MiB factory app at `0x10000` |
| TUNER//01 | `18ddd3b16e305341f338afebd7dc725500ecbb73` | 2,034,800 bytes (`0x1F0C70`) | `49f249ac0f6ea9f9d1e285ea15514ef5dc84483163c01edd1e052b2c8769bbd4` | `0x10000–0x200C6F` | unchanged 3 MiB `app0` at `0x10000` |

The REMOTE seven-entry partition binary remains SHA-256 `a144343580dbdadace66fccc5969d7557de3d4c4f15a61e76db205cc26348184`. The TUNER five-entry partition binary remains SHA-256 `aaae2888c5a6a348004b5b436f47abb25ae32e72d9003902955a998eda723edd`. Neither partition binary is a commissioning write input. Do not write either bootloader, either partition table, TUNER OTA metadata, REMOTE OTA metadata, or unrelated NVS.

Known REMOTE recovery evidence must remain private:

- retained 16 MiB backup: 16,777,216 bytes, SHA-256 `f6d806e0c19e545951f2e75ab8b9373a89215a58f2cb8b0a3c21f3d759e3bdb8`;
- retained prior factory restore span: 2,506,752 bytes, SHA-256 `57736494ea726600c68e25ae6a8f5b3bd109f5e5c1d5d858a05afd7ee8603aca`;
- retained original pre-A-009 table sector: SHA-256 `4946a42576c9e499c4a856b9104abfb6d09fff4f3fff2cd7985649ccbcec8f46` (recovery evidence only; it must not be written in this task).

The old REMOTE full backup predates the installed seven-entry table and the current generation-2 `remote_ctl` records. It is a last-resort recovery artifact, not the normal A-011 rollback image. The installed TUNER firmware identity is not currently proven. Therefore Stage 1 must create fresh private readbacks before any write:

1. full physical flash from each device;
2. each complete application partition;
3. TUNER default NVS (`0x9000–0xDFFF`);
4. REMOTE `remote_ctl` (`0xE20000–0xE2FFFF`).

Record byte counts and SHA-256 values twice and copy each verified backup to separate owner-controlled storage. The exact pre-write bytes over each candidate write range are the primary firmware rollback files. Do not proceed if a backup is truncated, unexpectedly all `0x00`/`0xFF`, unreadable, or lacks its separate-storage copy.

## Commissioning mechanism inspection and gate

The accepted implementation does **not** contain a pairing provisioning mechanism:

- TUNER `loadPairing()` opens default-NVS namespace `remote_pair` read-only and requires exact 16-byte `pair_id` and 32-byte `psk` values.
- REMOTE `association::load()` opens `remote_ctl` read-only and requires a valid A-010 record whose payload is the exact 68-byte A-011 association envelope.
- REMOTE `reserve_session()` may only advance an already valid association. It cannot create one.
- Neither firmware exposes a serial, web, network, or UI pairing writer. Existing REMOTE A-010 diagnostics accept only fixed persistence-test commands and must not be repurposed.

Pairing cannot safely be executed with the accepted candidates alone. Do not patch raw NVS bytes or publish a credential-bearing image. Before pairing, obtain separate owner approval for a minimal private one-shot commissioning helper that uses the same `Preferences` and A-010 backend APIs as production, verifies readback, never prints secret values, and disables itself after success. Review and build that helper before hardware use.

At authorized execution time, generate exactly one random 16-byte pairing identifier and one random 32-byte PSK from the operating system CSPRNG. Keep them only in a private owner-controlled provisioning file, never in Git, shell history, command-line arguments, logs, screenshots, or reports. Configure a stable private-LAN IPv4 address for TUNER through an owner-controlled DHCP reservation; record it privately with RTCP port `46411`. Provision:

- TUNER: namespace `remote_pair`, exact keys `pair_id` (16 bytes) and `psk` (32 bytes), preserving every unrelated default-NVS key;
- REMOTE: a version-1 68-byte association envelope containing magic `A11A`, port `46411`, TUNER IPv4, the same pairing identifier and PSK, and initial session generation `1`, committed through the validated A-010 backend in `remote_ctl`.

Before provisioning, confirm that fresh NVS/`remote_ctl` backups are verified. After provisioning, verify only structural success and hashes that do not reveal credential values. Never log or publish the envelope, namespace values, PSK, pairing identifier, IP/MAC, or raw partitions. Stop if the writer cannot preserve unrelated records or if readback is not exact.

## Staged execution

### Stage 1 — read-only identity and rollback capture

This is the first hardware operation and requires explicit owner approval.

1. Connect one device at a time. Enumerate ports, identify the expected chip through ROM/USB, record sanitized chip/revision/flash-size/tool identity, and bind the private evidence to the exact port. Do not rely on a port name alone.
2. Read and decode each installed partition table. Require exact agreement with its accepted layout. REMOTE must retain all seven entries and TUNER all five entries.
3. Create and independently verify all fresh backups listed above. Preserve the REMOTE generation-2 `remote_ctl` bytes and all TUNER configuration bytes.
4. Read the installed application image identity where possible. Do not claim source equivalence from a version string.
5. Verify ROM/USB recovery access for both devices without writing or erasing.
6. Stop for owner review. No flash or provisioning follows automatically.

### Stage 2 — application-only candidate installation

Requires separate owner approval after Stage 1 PASS.

1. Reverify candidate and rollback hashes immediately before writing.
2. Write only the REMOTE candidate at `0x10000`, using keep/preserve settings for detected flash mode, frequency, and size. Read back exactly `0x266280` bytes and require the candidate SHA-256.
3. Boot REMOTE normally. Require normal UI, stored configuration, Wi-Fi, sleep/wake behavior, and unchanged `remote_ctl` hash. The unpaired transport must remain disabled without storage writes.
4. Write only the TUNER candidate at `0x10000` with the same keep/preserve rule. Read back exactly `0x1F0C70` bytes and require the candidate SHA-256.
5. Boot TUNER normally. Require v1.1.11 MP3, Bluetooth A2DP, Wi-Fi, web manager, UI/control behavior, and unchanged default-NVS hash. The unpaired RTCP server must remain disabled.
6. Stop for owner review.

### Stage 3 — private pairing provisioning

Requires the separately reviewed helper and explicit owner approval. Run exactly once. Preserve the generation-2 REMOTE record as history; the association becomes a successor record through the existing backend. Verify the TUNER keys and REMOTE association structurally without exposing their values. Stop immediately on partial, ambiguous, or unexpected storage state. Do not retry a failed mutation.

### Stage 4 — authenticated read-only negotiation

After normal boots, allow the single persistent RTCP/1 connection. Before any control request, require mutual authentication and a fresh session; accepted device identity and CCM/RTCP version negotiation; the exact bounded capability snapshot; fresh `volume.level` and `playback.state` with valid sequence/media-generation progression; and no payload, credential, or unexpected storage error. Record only sanitized state/result codes and counters. Any authentication, identity, capability, freshness, counter, or resynchronization failure blocks control.

### Stage 5 — one controlled `volume.set`

Requires explicit owner approval after Stage 4 PASS. Record the initial volume, choose one adjacent valid grid value within the safe audible range, and send exactly one `volume.set`. Require one correlated success result and a fresh snapshot showing the requested value. Do not retry automatically. Restore the initial volume only by direct owner control unless a second network command is separately authorized.

### Stage 6 — reconnect and resynchronization

Use a reversible network interruption, not a power or flash operation. Interrupt the established connection once, restore connectivity, and require a new authenticated session, a newly reserved non-reused REMOTE session generation, renewed identity/capability validation, and fresh state before READY. Confirm no command replay and no automatic repetition of Stage 5.

### Stage 7 — TUNER coexistence measurements

Use the existing read-only serial `x` diagnostic snapshot; no new firmware instrumentation is needed. With the web manager active, capture a bounded baseline and then snapshots during stable MP3 playback and stable Bluetooth A2DP playback. Exercise one ordinary read-only web status request in each mode and capture another snapshot. Record:

- `heap_internal_free`;
- `largest_block`;
- `allocator_region_minimum`;
- `main_task_stack_hwm` and `audio_task_stack_hwm` (FreeRTOS words; report bytes only if platform word size is also recorded);
- allocation-failure count, web-response failure/overflow state, reset/watchdog state, audio continuity, and UI responsiveness.

Stop on allocation failure, watchdog/panic/reset, audio dropout attributable to RTCP, web-manager regression, stack high-water mark at or below the platform safety threshold, or internal free/largest-block readings insufficient for stable operation. Report observed values without turning this bounded check into a soak or industrial campaign.

## Exact rollback

Rollback is triggered by boot failure, partition error, UI/configuration loss, pairing inconsistency, RTCP authentication/state failure, audio/web regression, unsafe memory margin, or an unexpected persistent change.

1. Stop network commissioning and disconnect the peer. Do not erase either device.
2. If failure occurred before provisioning, restore only the exact candidate write range from the fresh pre-write range backup: REMOTE `0x10000–0x27627F` or TUNER `0x10000–0x200C6F`. Read it back and require byte and SHA-256 equality with the private rollback file.
3. If provisioning occurred, first preserve the failed state as a private readback. Restore TUNER default NVS (`0x9000–0xDFFF`) and REMOTE `remote_ctl` (`0xE20000–0xE2FFFF`) from their fresh pre-provision backups, then verify byte identity. This restores unrelated configuration and the REMOTE generation-2 records exactly.
4. Restore each written application range as in step 2. Never write a bootloader, partition table, OTA metadata, other NVS region, or full-flash image without new owner approval.
5. Attempt one normal boot per affected device. Require the prior UI, configuration, MP3/A2DP/Wi-Fi/web behavior, and expected unpaired state. Stop after one bounded rollback attempt and report.

## Stop conditions and publication

Stop on identity/layout mismatch, missing or unverifiable rollback material, unexpected flash size, inability to preserve existing records, absent provisioning-helper approval, secret exposure, candidate/readback mismatch, unexpected partition mutation, or any functional/memory failure above. Publish only sanitized hashes, counts, ranges, state transitions, and verdicts. Raw flash/NVS/`remote_ctl`, binaries, PSK, pairing identifier, IP/MAC, credentials, and private paths remain private.

## Next owner decision

Authorize or reject **Stage 1 only**: read-only access to both devices, exact identity/layout inspection, and creation plus verification of fresh private rollback backups. This authorization would not permit flashing, provisioning, pairing, NVS/`remote_ctl` mutation, control commands, or resets beyond those required for read-only ROM/USB access.
