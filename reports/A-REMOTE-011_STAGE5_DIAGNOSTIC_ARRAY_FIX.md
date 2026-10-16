# A-REMOTE-011 Stage 5 diagnostic array-size correction

Date: 2026-10-15  
Status: PRODUCTION BUILD PASS / NOT INSTALLED

The private diagnostics Core declaration contained 39 entries while both the initializer and JSON field-name table contained exactly 40. The declaration alone was corrected from 39 to 40. Field order, field types, admission decisions and diagnostic semantics were unchanged.

Exactly one production `remote01` build was run and passed. Previously passing focused tests were not repeated because their inputs did not change.

- Application size: 2,520,640 bytes
- SHA-256: `9edbfc968dbfe3dea66ab4d8932bb2e9389df670874510264b99fc9b5b51f98a`
- 3 MiB OTA-slot headroom: 625,088 bytes
- PlatformIO static RAM: 47,212 bytes
- PlatformIO flash usage: 2,520,133 bytes

The candidate retains the original brightness-slider behavior, authoritative HOME volume label/bar and bounded read-only encoder/admission diagnostics described in the preceding implementation record.

No hardware access, flash operation, live command, TUNER change, GPIO/NVS/pairing/protocol change, private source/binary publication or PR merge occurred. Installation and one controlled encoder-detent diagnostic test require separate owner authorization.

