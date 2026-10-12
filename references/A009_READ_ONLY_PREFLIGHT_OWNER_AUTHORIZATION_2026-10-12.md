# A-REMOTE-009 preparation acceptance and read-only preflight authorization

Recorded UTC: 2026-10-12T18:50:09.272297+00:00. Reviewed preparation head `bd5682d327448696f659000f40ae4b50ab16eeb4`; PR15 remains OPEN/unmerged.

The owner accepts the A009 preparation result and explicitly authorizes execution through the read-only hardware preflight and backup verification only: exact device/COM identification before access, chip/MAC/USB/physical-flash/tool identity recording privately, serial monitoring and read-access resets, complete16MiB backup, independent installed-table read/decode and byte comparison with A007, complete64KiB target read, read-only firmware/OTA identity and ROM/USB availability confirmation.

No flash write, erase, partition-table update, firmware upload, NVS mutation, rollback or recovery write is authorized. Stop before the first persistent write and request explicit owner approval against the actual verified backup and proposed table write. Do not start A010 or implement a backend/API; do not reopen A008 or harmless-build-difference forensics. Publish only sanitized hashes/structural results/verdict in English; no backup, private REMOTE source, NVS/credentials, MAC or unique device/USB data. Keep PR15 OPEN and unmerged.

Owner confirms REMOTE USB connection and closed monitors. Only local C: storage is currently available; owner explicitly chooses preservation of both verified reads locally, with the separate-storage backup copy deferred as a mandatory prerequisite before any future write. That exception authorizes no hardware write.

Preparation is OWNER ACCEPTED; read-only preflight authorization supersedes the prior hardware-NOT-AUTHORIZED label only for these reads/resets. Persistent operations remain NOT AUTHORIZED. The published preparation report/protocol are preserved historically and the new execution report records actual read-only results and any narrow authorized transfer-rate variation. Full write-based rollback remains NOT TESTED.

Owner explicitly keeps the published115200baud for both complete flash reads; no transfer-rate increase authorized or applied.
