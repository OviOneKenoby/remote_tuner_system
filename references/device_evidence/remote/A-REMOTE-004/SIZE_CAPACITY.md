# A-REMOTE-004 size/capacity verdict

Exact encoded bytes are MEASURED HOST CODEC facts,not target RAM,NVS entries or physical atomicity. Maximum derivation is machine-readable in results/MEASUREMENTS.json and reproducible in prototype/run_qualification.py;max fixtures attain the legal upper bounds.

| Complete fixture | Bytes |
| --- | ---: |
| typical_pending | 1405 |
| typical_resolved | 1601 |
| maximum_pending | 5587 |
| maximum_resolved | 6383 |
| maximum intermediate one-proof |5985|

Maximum future full-state growth796bytes;each proof contributes398. Full-state max6383bytes;BASE node6447,PROOF node1146,ALLOC node162,trusted root76. Four tail slots reserve both remaining proofs;do not confuse398-byte interned state growth with1146-byte independent log node.

Raw record reserve=2*6447+2*1146+2*162=15510bytes. That conservatively covers old+new complete snapshots plus two proof and two allocation tail records;four allocation-only tail nodes are smaller. Actual saturated initial snapshot+two proofs+new full compaction snapshot peaked at14390fake-record bytes. Fake data budget admission below15510 refuses before simulated handover. Root service/physical overhead is separate,not omitted from the NVS model.

## Existing partition first

Verified current partitions.csv:NVS0x9000,size0x6000=24576bytes,six4096byte pages. Installed pinned SDK5.5.3 Page has126entries/page,32bytes/entry,CHUNK_MAX_SIZE4000. Individual blob optimistic limit5*4000=20000,so6447 fits that limit. Setter writes new chunks/index before erasing old version;commit is not a multi-key transaction. SOURCE_SDK_SHA256 pins checked SDK/source;A003/A002 immutable evidence preserved.

E(blob)=ceil(bytes/32)+ceil(bytes/4000)+1,an OPTIMISTIC lower bound;partial tail chunks/fragmentation can require more. Two snapshots overlap;inactive is erased before replacing,so no third old inactive snapshot is assumed. Include two proof/two allocation nodes,OLD+NEW roots,12metadata entries,one126-entry GC page,old+new assumed other occupancy. Existing credential/driver/other namespace contents were NOT read;synthetic0/512/1024/2048/4096byte cases only. Actual free entries/space fragmentation/key counts/root service overhead are UNKNOWN. Root two-version footprint is an assumption,not a qualified anti-rollback implementation.

| Other occupancy assumption | Peak entries lower bound | Pool | Margin if exact | Optimistic fit |
| ---: | ---: | ---: | ---: | --- |
| 0 | 650 |756|106|True |
| 512 | 686 |756|70|True |
| 1024 | 718 |756|38|True |
| 2048 | 782 |756|-26|False |
| 4096 | 912 |756|-156|False |

Verdict:CURRENT24KiB is CONDITIONALLY PLAUSIBLE in lower-occupancy ideal cases,NOT physically qualified. It FAILS even the optimistic2048/4096byte old/new occupancy cases. The small70entry margin at512bytes and38at1024bytes cannot absorb unknown fragmentation/root costs by assumption. Production capacity verdict remains BLOCKED until measured free stats,real key/GC/overlap/root-service footprint and reserve are qualified. No credential values were inspected and no partition changed.

## Larger partition alternative ONLY

Hypothetical32KiB gives1008entries,which would fit this912entry lower-bound4096case with96entry margin;48KiB gives1512entries. These are arithmetic alternatives,not approved safe layouts. Existing NVS cannot simply expand in place:PHY0xF000/factory0x10000 would overlap. A separate control-storage partition in an independently approved layout/migration may avoid touching remote_wifi,but must be separately assigned and power-cut qualified. No CSV/configuration/layout/migration change is made. Extra capacity would NOT solve newest-intent integrity.

Target flash/RAM/frame/task delta0 from this work because no target-selected files changed;future target codec/importer/buffer/stack costs UNKNOWN. Python heap/resource/runtime observations are not ESP32 costs. No target build or new firmware hash claimed;hardware NOT RUN.
