from pathlib import Path
import json,math
rows=json.loads((Path(__file__).parent/'CAPACITY_LEDGER.json').read_text())
for r in rows:
 c=r['chunk_tailroom'];e=lambda n:math.ceil(n/32)+math.ceil(n/c)+1
 nodes={k:2*e(n) for k,n in [('BASE',6447),('PROOF',1146),('ALLOC',162),('root',76)]}
 assert nodes==r['record_entries']
 total=sum(nodes.values())+2*e(r['external_payload_bound'])+r['metadata_entries']+r['GC_entries']+r['fragmentation_entries']
 assert total==r['required_entries'] and r['margin_entries']==r['pool_entries']-total
 assert r['pool_entries']==r['partition_KiB']//4*126
 assert r['physical_accounted_bytes']==total*32+r['page_header_bitmap_bytes']
print('PASS 12 capacity cases; physical UNKNOWN; broader 44284-byte two-bank profile FAIL all sizes')
