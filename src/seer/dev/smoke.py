import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import nodes.seer as m
from subsets_utils import load_raw_ndjson

sid = "seer-prevalence-complete"
m.fetch_one(sid)
rows = load_raw_ndjson(sid)
print("rows:", len(rows))
print("sample:", rows[0])
print("distinct sites:", len({r.get("site") for r in rows}))
print("columns:", sorted(rows[0].keys()))
