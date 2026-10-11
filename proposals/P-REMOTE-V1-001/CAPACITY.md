# Capacity remains an independent blocker
PROPOSED / NOT APPROVED. Analysis only, actual namespace occupancy/free entries/fragmentation UNKNOWN; no NVS read or partition change. Source constants: selected ESP-IDF5.5.3, page4096, entries126, entry32, per-page header/bitmap64, max blob chunk4000. This is a conservative declared-entry ledger, not the SDK allocator, endurance proof or physical PASS.

Minimum useful P4: one device/target, two bindings/conflict routes, one shared resource, two Favorites and one unresolved effect/attempt; complete required capture/proof/barrier/non-reuse data. Maximum supported legal *P4* state: pending5587, resolved6383 encoded bytes, proof/resolution growth796. Inherit unchanged A004 profile/codec restrictions: no recipes/numeric/assets/multiple effects/oversized strings; unsupported legal inputs refuse before handover, never truncate mandatory data. This does not establish production support for the full CCM legal space.

Peak old/new overlap reserves two BASE6447, two PROOF1146 and two ALLOC162 =15510 logical bytes; old/new generation roots76 each =152, total15662. Root slots stay even without strict anti-rollback service. Entries under4000-byte chunks: BASE410, PROOF76, ALLOC16, roots10 =512. Proof slots retain unresolved and resolved evidence; watermark/tombstones stay until their normative retirement. G1b exclusion removes no mandatory record and gives no claimed storage saving: previous service cost UNKNOWN, proposed strict service budget0.

Formula for a blob of n bytes: ceil(n/32)+ceil(n/chunk_tailroom)+1; each persistent category reserves two versions. Namespace/key metadata allowance12 ideal,32 planning; GC126 (one spare page) separately. Current `remote_wifi` schema108 bytes reserves12 entries old/new. Planning bounds total external payload4096 including remote_wifi/other namespaces, two versions262 entries (274 at512-byte tailroom); no credentials read. Fragmentation252 entries (two stranded pages) is additional to GC. Chunk512 sensitivity uses538 record/root entries versus512. These budgets must be enforced or measured before acceptance; unrestricted occupancy/fragmentation cannot be solved by a finite partition recommendation.

| KiB | Pool entries | Ideal required / margin | Planning required / margin | Partial chunks required / margin |
| --- | --- | --- | --- | --- |
| 24 | 756 | 662 / 94 | 1184 / -428 | 1222 / -466 |
| 32 | 1008 | 662 / 346 | 1184 / -176 | 1222 / -214 |
| 48 | 1512 | 662 / 850 | 1184 / 328 | 1222 / 290 |
| 64 | 2016 | 662 / 1354 | 1184 / 832 | 1222 / 794 |

Recommended minimum planning pool: **48 KiB**, conditional on the declared P4/external/fragmentation bounds. At512 tailroom:1222/1512 entries, margin290 entries =9280 entry bytes (19.2% pool). 32 KiB fails with margin-214;24 fails-466. 64 KiB gives794 entries margin. Ideal24 fits662/756, but94 spare entries is inadequate for the declared planning envelope. Every fit remains MODEL CONDITIONAL, physical UNKNOWN. No anti-rollback mechanism is credited as NVS PASS.

Maximum wider A003 declared encoded state44284 needs at least88568 raw bytes for two complete overlapping payloads, before headers/root/proof/GC. All24/32/48/64KiB choices fail that two-generation full-bank profile. A future append design may change peak requirements only after an exact complete codec/compaction proof; no support claim or data deletion here. P4 is the maximum legal profile supported by this *analysis*, not a new normative CCM limit.

Do not expand the existing24KiB NVS in place: its0x9000 start/0x6000 size ends0xF000 and existing subsequent regions must be checked. A48KiB usable pool requires a separately designed partition allocation/layout, backup/migration/recovery plan and explicit authorization. Dedicated control storage changes external-occupancy assumptions and must be recalculated; this conservative comparison retains the shared-domain budget. No partition placement is approved here.

Reproduce: `python -B proposals/P-REMOTE-V1-001/check_capacity.py`; JSON ledger is the full comparison. Unbounded proof growth, outstanding effects, allocator retention and broader legal inputs remain pre-emission refusal cases until a separately qualified lossless profile covers them.
