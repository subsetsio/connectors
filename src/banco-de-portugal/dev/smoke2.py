import sys
sys.path.insert(0,"src")
import nodes.banco_de_portugal as m
from subsets_utils import load_raw_ndjson
# e2bc: 502 at ps 100 & 50, works at 25 -> should fall back and succeed
ds="e2bc3b33d169f2d0885cffb9183fb48e"
nid=f"banco-de-portugal-{ds}"
m.fetch_one(nid)
rows=load_raw_ndjson(nid)
print(f"e2bc rows={len(rows)} distinct_series={len({r['series_id'] for r in rows})} (expected 507)")
print("date range:", min(r['reference_date'] for r in rows),"->",max(r['reference_date'] for r in rows))
