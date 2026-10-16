# A-REMOTE-011 Stage 4: production restoration and authenticated read-only verification

## Result

**PASS — BOTH PRODUCTION APPLICATIONS RESTORED; AUTHENTICATED READ-ONLY RTCP/1 SYNCHRONIZATION VERIFIED.**

This report supersedes the Stage 4 stopped result while preserving it as historical evidence. The continuation repeated only the work blocked by the earlier COM5 access failure. REMOTE was not reflashed.

## Production restoration

- REMOTE: the accepted 2,515,584-byte application at `0x10000` had already passed exact readback against SHA-256 `ceae9f64329c5409fdfe92e5ac5394885010abf1cf66ac24a5ab7fcc35f11647`. Its boot evidence showed the expected factory application and a configured association with no unconfigured write.
- TUNER: COM5 was positively identified as the accepted classic ESP32 device with 4 MiB flash. The accepted 2,034,800-byte application, SHA-256 `49f249ac0f6ea9f9d1e285ea15514ef5dc84483163c01edd1e052b2c8769bbd4`, was written once at `0x10000` at 921600 baud with flash mode, frequency and size preserved. An independent readback of exactly 2,034,800 bytes matched the accepted SHA-256.
- No bootloader, partition table, OTA metadata, default NVS, `remote_ctl` or other flash region was supplied to either write command. Existing association records were preserved.

Both production applications booted normally. The TUNER reported its expected production identity, loaded stored network configuration and reached normal setup without a captured panic, watchdog or partition error. The owner confirmed normal UI and retained configuration on both devices.

## Authenticated read-only verification

The paired devices joined the same private LAN using their retained association data. REMOTE reported one active RTCP session. The implemented state machine can reach that state only after the fresh-nonce mutual PSK proof, directional key derivation and authenticated record setup succeed.

The mandatory negotiation sequence completed in order:

1. the identity response passed the RTCP parser's exact CCM version check for `1.1.0`;
2. the bounded capability response advertised `volume.level`, `playback.state` and `volume.set` with a nonzero revision and valid freshness bound;
3. authenticated snapshots containing bounded volume and playback values with nonzero sequence and media-generation fields continued to be accepted.

Two private read-only diagnostic snapshots three seconds apart showed the same active session, capability revision advancing from 232 to 240 and lifecycle evidence advancing from 58 to 60. This demonstrates continuing fresh synchronization. Command dispatches, rejected commands, invalid results, refused results and failed allocations remained zero. No `volume.set` or other RTCP control command was issued.

The diagnostics endpoint intentionally does not expose the private LAN addresses or current media values in the public evidence. Complete captures and hashes remain private.

## Scope and next gate

Stage 4 is complete at the approved practical hobby/public-beta assurance level. No source change, build, credential generation, pairing mutation, unrelated test or PR merge occurred during this continuation.

The next optional commissioning action is the separately gated single controlled `volume.set` described by the published procedure. It requires explicit owner authorization and was not executed here.
