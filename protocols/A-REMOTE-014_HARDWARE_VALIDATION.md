# A-REMOTE-014 controlled hardware validation

Status: **COMPLETED / PASS** (Functional hardware validation completed 2026-10-20).

## Preconditions

1. Verify the intended device through its ROM/USB identity; never infer it
   from a COM number.
2. Rehash the complete local and separate-storage rollback sets for both
   devices against their accepted manifests.
3. Rehash the exact private A-REMOTE-014 application candidate and confirm its
   size, source identity, application offset, and available partition space.
4. Preserve NVS, RTCP pairing, bootloader, partition table, OTA metadata, and
   all unrelated partitions. Use application-only writes and exact-span
   readback at the authorized baud rate.

## TUNER first

1. Install only the 2,069,152-byte TUNER candidate at `0x10000`.
2. Read back exactly 2,069,152 bytes and require SHA-256
   `d2c89edd1e5aa25a01c7f88ce787ccdcfa2e708a89d6fb402d0326a519ec896e`.
3. Verify normal boot, retained configuration/pairing, Wi-Fi, HTTP, MP3, A2DP,
   D-009 compatibility, and bounded internal heap/task margins.
4. Verify `_rtcp._tcp` advertises TCP 46411 only while listener and Wi-Fi are
   available and returns after a normal Wi-Fi reconnect.

## REMOTE second

1. Install only the 2,568,992-byte REMOTE candidate at `0x10000`.
2. Read back exactly 2,568,992 bytes and require SHA-256
   `cdfccacdf07d0e4ca0a29b2c92f3cf29ee5e1b65df109ca730c3915185c82e2d`.
3. Verify normal boot, retained UI/configuration/pairing, voltage telemetry,
   sleep/wake, and Wi-Fi.
4. With the saved stale endpoint unchanged, require automatic discovery,
   successful RTCP mutual authentication, READY state, authoritative volume
   and playback, `volume.set`, and D-009 compatibility.

## Network behavior

1. Cause one ordinary DHCP address change through owner-controlled network
   operation without changing NVS or re-pairing. Require automatic rediscovery
   and authenticated recovery.
2. Advertise a second `_rtcp._tcp` service without the pair PSK. Require its
   authentication rejection and eventual selection of the valid TUNER.
3. Suppress multicast once. Confirm bounded reconnect behavior and saved
   endpoint fallback; do not expect stale-endpoint recovery while multicast is
   unavailable.
4. Verify sleep/wake and Wi-Fi disconnect/reconnect invalidate the old runtime
   endpoint and recover without stale command replay.

## Stop and rollback

Stop on any identity/hash/readback mismatch, boot failure, unexpected NVS or
pairing change, authentication bypass, unbounded reconnect behavior, resource
failure, playback/HTTP regression, stale command replay, or failure to recover
the valid advertiser. Restore only the affected device's accepted application
image using the already verified application-only rollback procedure, then
verify exact readback and normal boot. Full-flash recovery remains separately
authorized only when necessary.

Record all observed addresses only in private evidence. Publish sanitized
hashes, counters, structural results, and PASS/FAIL classifications.
