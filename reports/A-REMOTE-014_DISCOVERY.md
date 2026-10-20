# A-REMOTE-014 automatic RTCP discovery report

Date: 2026-10-20
Status: **HARDWARE VALIDATED / PASS**
Coordination input: `5d36f06c301cdd340fe65084dca4d636ad6dc699`

## Problem and design

The physical pair retained valid RTCP association keys, but DHCP moved TUNER
from its stored address to a new address. The existing literal endpoint could
not recover. A-REMOTE-014 uses standard multicast DNS/DNS-SD for service type
`_rtcp._tcp` while preserving the existing RTCP/1 security boundary.

TUNER uses its pinned Arduino `ESPmDNS` 2.0.0 support. It advertises TCP port
46411 only while the RTCP listener and Wi-Fi are available, stops the service
on disconnect, and retries a failed start every five seconds. Its hostname is
derived from a bounded hardware suffix. It publishes no TXT record, pairing
identifier, key, credential, token, station metadata, or user data.

REMOTE uses official Espressif `mdns` 1.14.0, locked for ESP-IDF 5.5.3. A fixed
6,144-byte static application worker performs a 750 ms PTR query at most every
five seconds, accepts at most four results, filters for IPv4, port 46411, and a
nonzero TTL, and removes duplicates. The saved endpoint remains a fallback.
Candidates rotate after pre-authentication failures. A candidate becomes the
runtime endpoint only after the existing PSK proof and encrypted identity
response succeed. A previously authenticated endpoint is unpinned if a later
connection fails before authentication, allowing rediscovery after DHCP
movement. Confirmed Wi-Fi loss, network-generation change, and sleep clear
runtime discovery state. No discovered address is persisted.

## Security and failure behavior

mDNS is unauthenticated, so an announcement is treated only as an address
hint. Spoofed and unrelated devices cannot become the paired authority without
the existing RTCP PSK and identity. Candidate count, query duration, cadence,
buffers, and the application worker are bounded. RTCP replay protection,
session fencing, timeouts, CCM validation, command correlation, and the
single-command-in-flight rule are unchanged.

If multicast is blocked or discovery initialization fails, REMOTE retains the
existing saved-endpoint reconnect behavior. This preserves compatibility but
cannot recover a stale saved address on a multicast-blocked network. Multiple
advertisers are tried within the four-candidate bound; authentication selects
the paired TUNER.

## Verification

| Device | Check | Result |
| --- | --- | --- |
| TUNER | Advertisement lifecycle model | PASS 9/9 |
| TUNER | Discovery source-policy checks | PASS 6/6 |
| TUNER | Existing D-009 focused tests | PASS 23/23 |
| TUNER | Existing D-009 integration policy | PASS 12/12 |
| REMOTE | Endpoint selection, changed address, candidates, fallback | PASS 10/10 |
| REMOTE | Discovery/security/lifecycle source policy | PASS 10/10 |
| REMOTE | Network-status regression | PASS 15 checks / 142 assertions |
| REMOTE | RTCP association and wire regression | PASS 11/11 |
| REMOTE | RTCP lifecycle policy | PASS 13/13 |
| TUNER | Flash write (`0x10000`) & independent 115200-baud readback | PASS byte-exact match `d2c89edd...` |
| TUNER | DNS-SD PTR/SRV/A advertisement query | PASS `tuner-641d44.local:46411` -> `192.168.1.31` |
| TUNER | MP3 playback through headphones & HTTP 200 response | PASS |
| REMOTE | Flash write (`0x10000`, `factory`) & independent readback | PASS byte-exact match `cdfccacd...` |
| REMOTE | Prior installed application readback vs known rollback | PASS byte-exact match `b6053c04...` |
| Pair | Paired startup, UI, encoder volume control to headphones | PASS |
| Pair | Power-loss & reconnect recovery across DHCP change | PASS (`192.168.1.152` -> `192.168.1.31`) |
| Pair | MP3 status display (`Playing`) & volume post-restart | PASS |

## Hardware Validation Results

1. **TUNER Verification:** Flashed 2,069,152 bytes at `0x10000` (ESP32-D0WDQ6-V3 / ESP32-WROVER). Independent 115200-baud readback SHA-256 matched `d2c89edd1e5aa25a01c7f88ce787ccdcfa2e708a89d6fb402d0326a519ec896e`. MP3 audio via headphones and HTTP 200 OK passed. DNS-SD interrogation confirmed PTR `_rtcp._tcp.local` -> `tuner-641d44._rtcp._tcp.local`, SRV `tuner-641d44.local:46411`, A `tuner-641d44.local` -> `192.168.1.31`.
2. **REMOTE Pre-Flash Rollback Verification:** Read 2,526,848 bytes before flash; SHA-256 matched `b6053c04c03114a24a59f178da4eb03d4bada77faded43b6009667579c21d5da` exactly against known rollback image.
3. **REMOTE Verification:** Flashed 2,568,992 bytes at `0x10000` (`factory` partition) on ESP32-S3 (16 MiB Flash / 8 MiB PSRAM, COM3). Independent readback SHA-256 matched `cdfccacdf07d0e4ca0a29b2c92f3cf29ee5e1b65df109ca730c3915185c82e2d` exactly. Both `otadata` entries remained erased (`0xFFFFFFFF`). NVS, partition table, bootloader, OTA metadata, and `remote_ctl` partitions were preserved.
4. **Integration & Automatic Recovery:** REMOTE recovered connection to TUNER at new IP `192.168.1.31` (previously `192.168.1.152`) without manual re-pairing or IP configuration. UI, encoder volume control, headphone volume updates, disconnect detection on TUNER power loss, auto-reconnect on TUNER power-on, and MP3 status display (`Playing`) all passed on physical hardware.

## Production artifacts

| Item | TUNER | REMOTE |
| --- | --- | --- |
| Executable source | `63ff6770fe4f0d7a46cb547ddc8f14abaec7f0fc` | `9c805e5444587bc3d8952a57f44ec526c615e74a` |
| Environment | `esp32-lwip-psram` | `remote01` |
| Build | PASS | PASS, clean |
| Embedded project build identity | `63ff6770fe4f` | `9c805e5` |
| Application size | 2,069,152 bytes | 2,568,992 bytes |
| SHA-256 | `d2c89edd1e5aa25a01c7f88ce787ccdcfa2e708a89d6fb402d0326a519ec896e` | `cdfccacdf07d0e4ca0a29b2c92f3cf29ee5e1b65df109ca730c3915185c82e2d` |
| Static RAM | 89,832 / 327,680 bytes | 56,356 / 327,680 bytes |
| Slot headroom | 1,076,576 bytes | 577,056 bytes |
| Baseline delta | +28,448 binary; +1,928 RAM | +42,144 binary; +8,968 RAM |

TUNER's official mDNS task uses a 4,096-byte stack. REMOTE adds a fixed
6,144-byte application worker, while the official component also owns its
4,096-byte mDNS task. Query-result allocations are library-owned and bounded
by four results; exact peak runtime heap use is not measured without hardware.
TUNER service-record allocation is likewise framework-owned and its exact
runtime peak is not measured. Both binaries fit their unchanged partitions.

The TUNER [PR #8](https://github.com/OviOneKenoby/ESP32-WROVER-Internet-radio/pull/8)
is stacked on the D-009 PR #7 head, which remains untouched. REMOTE
[PR #3](https://github.com/OviOneKenoby/REMOTE-01/pull/3) starts from public
`main`. Coordination evidence is in
[PR #23](https://github.com/OviOneKenoby/remote_tuner_system/pull/23).
All three remain open and unmerged. Candidate binaries are retained privately
and are not published.

## Remaining validation / Evidence limitations

- REMOTE internal resolver packet trace (no packet capture collected; functional proof established via endpoint recovery).
- Deliberately forcing a second DHCP address change during operation.
- Long-duration soak testing or repeated reconnection cycles.
- Bluetooth A2DP regression testing under mDNS advertisement.
- Runtime heap/PSRAM watermarks or long-term memory stability telemetry.

## Recommendation

**GO for separately authorized, controlled TUNER-first application-only
commissioning.** This is a software-readiness recommendation, not hardware
acceptance. Stop and roll back the affected application on identity, readback,
boot, resource, playback, discovery, authentication, or lifecycle failure.
