import sys, os, json, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import nodes.seer as m
from subsets_utils import load_raw_ndjson
import duckdb

sid = "seer-survival-long-term-trends"  # a failing transform
m.fetch_one(sid)
rows = load_raw_ndjson(sid)
print("rows:", len(rows), "cols:", sorted(rows[0].keys()))
# per-column python types
types = collections.defaultdict(collections.Counter)
nonnum = collections.defaultdict(list)
for r in rows:
    for k,v in r.items():
        types[k][type(v).__name__]+=1
        if isinstance(v,str) and k not in ('sex','race','age_range','stage','subtype','site','survival_time_interval'):
            nonnum[k].append(v)
for k,c in types.items():
    print(f"  {k}: {dict(c)}")
print("non-numeric strings in measure-ish cols:")
for k,vs in nonnum.items():
    print("   ", k, set(vs[:10]))
