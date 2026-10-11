# Complete declared-profile capacity ledger
[Machine ledger](results/CAPACITY_LEDGER.json) contains180 assumption combinations, from exact A004 P4 codec constants rechecked against current SDK. Six4096-byte pages at NVS0x9000/0x6000.126 entries/page,32 bytes/entry; header+bitmap64 bytes/page; CHUNK_MAX_SIZE4000. SDK reserves a page for GC. These are source facts, not available-entry measurements.

Minimum useful complete declared P4 profile: one device/target, two bindings, one shared resource, two Favorites, one unresolved effect/attempt with both conflict routes, required captures/proofs/barriers/non-reuse facts; source mappings inherited unchanged from A004 PROFILE_AND_TRACE. Unsupported association/recipes/numeric/assets/multiple effects/oversized text refuse before handover; no fields truncated. Typical P4 encoded pending1405/resolved1601; saturated legal pending5587/resolved6383, resolution growth796. P4 does not claim support for all production legal inputs: complete wider A003 max44284 remains infeasible at24KiB and unsupported by narrower profile.

| Category | Accounted separately |
| --- | --- |
| Payload encoded | maximum legal P4 state6383; pending5587; proof growth796 |
| Peak live logical records / compaction reserve | two complete BASE6447 + two independent PROOF1146 + two ALLOC162 =15510 bytes; original measured compaction peak14390 is smaller |
| Logical root/anchor | old+new76-byte roots =152; total logical record/root reserve15662; external root-service implementation cost UNKNOWN |
| Physical record/root entry lower bound | BASE410 + PROOF76 + ALLOC16 + root10 =512 entries under4000-byte chunk assumption |
| Namespace/index/metadata allowance | 12 entries separately; each blob formula includes chunk headers/index.12 is declared allowance, not measurement of actual keys/unknown namespaces |
| GC / recovery reserve |126 entries (one spare page); old/new complete generations and both proof slots retained; no live barrier eviction |
| Existing remote_wifi | source current schema encoded Blob108, name remote_wifi; old+new update assumed12 entries. Actual saved values/length/free stats NOT READ. Wi-Fi nvs_enable=0 in network manager does not prove no other occupancy |
| External occupancy | scenarios0/108/512/1024/2048/4096 bytes with old+new overlap; actual namespaces UNKNOWN |
| Fragmentation | stranded0/32/64/126/630 entries, chunk tailroom4000 or512 sensitivity. They are conservative scenario allowances, not an exact page allocator/emulator |
| Independent root footprint | extra0/32/126 entries sensitivity; no qualified root implementation, actual overhead UNKNOWN |
| Physical update peak | reserve-inclusive required entries *32 plus six64-byte headers/bitmaps; compare756-entry/24576-byte pool. Includes update overlap, root versions, proof growth, external overlap, metadata and GC; not a measured flash peak |

Ideal108-byte remote_wifi case:662 entries, physical account21568 bytes, margin94 entries.512 case686,1024 case718;2048 case782 FAIL and4096 case912 FAIL.108 plus126 stranded entries needs788 FAIL. Extra trusted-root cost126 also fails. More aggressive fragmentation/partial chunks may fail sooner; no claim of physical fit. Raw logical bytes15510 are not interchangeable with physical NVS capacity. Actual capacity verdict CONDITIONAL ideal cases / FAIL adverse cases / UNKNOWN physical; production BLOCKED. Partition expansion not executed and would not solve G1.
