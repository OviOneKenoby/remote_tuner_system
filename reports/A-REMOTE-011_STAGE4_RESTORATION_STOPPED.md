# A-REMOTE-011 Stage 4: production restoration stopped

## Result

**STOPPED — REMOTE RESTORATION PASSED; TUNER RESTORATION DID NOT START BECAUSE COM5 WAS BUSY.**

The owner-authorized Stage 4 procedure stopped on its first unexpected failure. No automatic retry was made. Authenticated read-only RTCP/1 verification was not reached.

## Preconditions

- Both accepted production images matched their required sizes and SHA-256 values before use.
- Every manifest-listed Stage 1 REMOTE and TUNER rollback file was present and matched its recorded byte length and SHA-256.
- The connected interfaces had already been positively identified as the accepted ESP32-S3 REMOTE with 16 MiB flash and classic ESP32 TUNER with 4 MiB flash. Device identifiers remain private.

## REMOTE restoration

The 2,515,584-byte REMOTE production application, SHA-256 `ceae9f64329c5409fdfe92e5ac5394885010abf1cf66ac24a5ab7fcc35f11647`, was written once at `0x10000` using 921600-baud esptool communication with flash mode, frequency and size preserved. No separate erase or non-application image write was issued.

An independent readback of exactly 2,515,584 bytes matched the accepted SHA-256. The boot log confirmed the application at `0x10000`, no observed panic/watchdog/partition error in the capture, and `A011_RTCP configured=1 unconfigured_write=0`, showing that the association remained configured without a provisioning write. Owner-visible UI/configuration confirmation remains pending because the procedure stopped before the combined Stage 4 completion check.

## TUNER stop condition

The accepted 2,034,800-byte TUNER production image matched SHA-256 `49f249ac0f6ea9f9d1e285ea15514ef5dc84483163c01edd1e052b2c8769bbd4` immediately before the attempted command.

Esptool failed while opening COM5 with the operating-system error `Access is denied`. The failure occurred before ROM connection, erase or write. Therefore:

- zero TUNER flash bytes were written in Stage 4;
- the corrected TUNER commissioning helper remains installed;
- the provisioned TUNER pairing store was not restored, erased or otherwise modified;
- no RTCP command or authenticated read-only session was attempted.

## Next gate

Stage 4 is incomplete. The minimum next action is to identify and close the process holding COM5, reverify the port and accepted TUNER image, and obtain a new owner decision for the unexecuted TUNER application-only restoration plus the remaining read-only checks. REMOTE must not be reflashed again unless a separate concrete need is found.
