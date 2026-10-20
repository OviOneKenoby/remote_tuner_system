# A-REMOTE-014 automatic RTCP discovery report

Date: 2026-10-20  
Status: **SOFTWARE READY / HARDWARE NOT VALIDATED**  
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

These are host and source-policy results. No device, router, multicast network,
or DHCP server was exercised in A-REMOTE-014.

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

## Remaining validation

- Physical advertisement and discovery on the target LAN.
- Automatic recovery from the observed stale saved endpoint and a subsequent
  DHCP address change without NVS edits or re-pairing.
- Multiple and spoofed advertiser behavior with real RTCP authentication.
- Multicast-loss fallback, sleep/wake, and Wi-Fi reconnect behavior.
- MP3, A2DP, HTTP, D-009, volume, UI, and resource regression on the pair.
- Runtime heap/task watermarks for both mDNS implementations.

## Recommendation

**GO for separately authorized, controlled TUNER-first application-only
commissioning.** This is a software-readiness recommendation, not hardware
acceptance. Stop and roll back the affected application on identity, readback,
boot, resource, playback, discovery, authentication, or lifecycle failure.
