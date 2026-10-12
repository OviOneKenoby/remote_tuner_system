# A009 owner authorization: backup-bound table-only write

Owner decision supplied 2026-10-12; recorded 2026-10-12T20:24:27.882825+00:00. Reviewed coordination input `1e549d4d6be00c77d61c020adf0b82ed4a04e729`. This versioned record supersedes the earlier read-only prohibition only for this approved operation. It does not rewrite historical protocol authority.

Owner authorizes candidate partitions.bin SHA256 `a144343580dbdadace66fccc5969d7557de3d4c4f15a61e76db205cc26348184` at0x8000, retaining flash mode/frequency/size. Recovery backup:16777216bytes/SHA256 `f6d806e0c19e545951f2e75ab8b9373a89215a58f2cb8b0a3c21f3d759e3bdb8`. Local primary reverified by executor. Owner independently reports a separate-storage Orange Pi copy with identical size/SHA; executor did not access that host or claim independent remote-copy verification. All absolute private paths and device identifiers remain restricted.

Before writing: rehash primary/candidate, confirm same A007/A009 ESP32-S3 on COM3 and ROM USB access, read/save/hash original4096-byte table sector. Only erase/program footprint `[0x8000,0x9000)` is authorized. No firmware upload, NVS/OTA/application/target-region writes, other-sector writes or standalone erase.

Post-write: full-sector candidate/padding readback, independent table decode with six unchanged records and new remote_ctl64KiB at0xE20000, unchanged3MiB OTA slots/bounds/alignment/no-overlap, reread complete64KiB target and require allFF, normal reset/passive boot capture and owner visual UI/configuration confirmation without settings mutation. Published protocol's full before-reboot preservation read retained.

Bounded rollback only upon table readback mismatch, decode failure, normal boot failure specifically after this operation or partition-table error: restore original verified4096-byte table sector at0x8000 once, byte-verify, attempt one normal boot, then stop/report. No repeated writes. **Historical protocol step9 full16MiB restore is NOT authorized by this decision.** A full restore requires separate owner approval.

Keep PR15 OPEN/unmerged. Publish only sanitized evidence/hashes; no private source, full backup, NVS, MAC, credentials or absolute private paths. No backend/common API/A010/TUNER/CCM work. Practical hobby/public-beta assurance; no industrial campaign. Interruption during table writing can prevent normal boot; verified backup and ROM USB are the recovery path. Actual restoration is not claimed tested unless performed.
