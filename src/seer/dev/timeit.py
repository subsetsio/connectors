import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import nodes.seer as m
from subsets_utils import load_raw_ndjson
sid = "seer-seer-incidence-recent-trends"  # largest: 73 sites, year series, all dims
t=time.time(); m.fetch_one(sid); el=time.time()-t
rows = load_raw_ndjson(sid)
print(f"{sid}: {len(rows)} rows in {el:.1f}s; sites={len({r.get('site') for r in rows})}")
