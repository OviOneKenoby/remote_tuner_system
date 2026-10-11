# Exact size and offline storage ledger

MEASURED means bytes produced by the standalone codec, not target RAM/NVS usage. SDK source facts come from installed pinned IDF5.5.3; offline arithmetic is an optimistic model, not a physical guarantee.

| Fixture | Payload | Envelope total | 3072-byte bank |
| --- | ---: | ---: | --- |
| typical_pending | 2730 | 2746 | FITS in isolation |
| typical_resolved | 3212 | 3228 | FAIL |
| maximum_pending | 35308 | 35324 | FAIL |
| maximum_resolved | 44268 | 44284 | FAIL |

Typical resolution growth: 482 bytes; 2746+482=3228, so even the typical complete growth allowance FAILS 3072. Maximum reserve: 8960; 35324+8960=44284. No sample-only assumption: recursive maximum derivation and enforced deductions are in MEASUREMENTS.json and runner. A hypothetical smaller text/evidence cap requires a separate complete-profile review and refusal/resolution qualification.

## Pinned SDK facts

A-002 immutable SDK snapshots were rechecked against installed source. nvs_storage.cpp:273 writeMultiPageBlob caps one blob at (partition pages-1)*Page::CHUNK_MAX_SIZE; six-page partition => optimistic individual ceiling20000 bytes. Both maximum fixtures exceed it before considering bank overlap. Page has126 entries of32bytes; CHUNK_MAX_SIZE4000. nvs_storage.cpp:273-376 writes new BLOB_DATA chunks, then BLOB_IDX, attempts chunk cleanup on error. :475-550 alternates chunk versions, writes new version then erases old version; failures can retain earlier contents or ambiguous new/old parts. nvs_handle_simple.cpp commit only checks validity then returns ESP_OK; it provides no multi-key transaction or extra physical power-loss barrier. Existing partition is24KiB; do not expand it or erase remote_wifi.

## Peak entry model

E(blob)=ceil(bytes/32)+ceil(bytes/4000)+1. This is optimistic: partial tail chunks/fragmentation can require more. Peak modeled entries=3*E(bank) +2*E(anchor46) +2*E(assumed credential bytes) +12 metadata entries +126 entries GC allowance. Three banks means active + old inactive + replacement-before-old-erasure; anchor previous/new overlap; old/new credential allowance avoids namespace-isolation fallacy. Catalog/proof growth already included in bank. Model assumes credentials represented as one blob; actual remote_wifi values/key counts/Wi-Fi-driver data/other namespace occupancy are UNKNOWN. Cases0/512/4096 are sensitivity assumptions, not inspected secrets. The whole physical pool is756 entries; reserved GC allowance is charged in peak.

| Bank bytes | Synthetic credentials | Peak entries | Lower-bound pages | Optimistic fit |
| ---: | ---: | ---: | ---: | --- |
| 3072 | 0 | 442 | 4 | True |
| 3072 | 512 | 476 | 4 | True |
| 3072 | 4096 | 702 | 6 | True |
| 2746 | 0 | 412 | 4 | True |
| 2746 | 512 | 446 | 4 | True |
| 2746 | 4096 | 672 | 6 | True |
| 3228 | 0 | 457 | 4 | True |
| 3228 | 512 | 491 | 4 | True |
| 3228 | 4096 | 717 | 6 | True |
| 35324 | 0 | 3490 | 28 | False |
| 35324 | 512 | 3524 | 28 | False |
| 35324 | 4096 | 3750 | 30 | False |
| 44284 | 0 | 4339 | 35 | False |
| 44284 | 512 | 4373 | 35 | False |
| 44284 | 4096 | 4599 | 37 | False |

Even an optimistic FIT is not feasible-capacity certification: free entries, tailroom, GC behavior, latency/endurance and power-loss retention are UNKNOWN. Maximal bank profile FAILS current storage. Target static RAM/task frame added=0 because nothing is target-selected; target codec peak buffers/frames are UNKNOWN (Python heap use is not an ESP measurement). No target compile/build run or existing artifact overwritten.
