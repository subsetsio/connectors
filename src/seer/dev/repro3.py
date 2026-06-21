import sys, os, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import nodes.seer as m
from subsets_utils import load_raw_ndjson
for sid in ["seer-risk-of-diagnosis-dying-risk-comparisons", "seer-us-mortality-rural-urban-rates"]:
    m.fetch_one(sid)
    rows = load_raw_ndjson(sid)
    colsets = collections.Counter(tuple(sorted(r.keys())) for r in rows)
    print(f"{sid}: {len(rows)} rows; distinct column-sets: {len(colsets)}")
    for cs,n in colsets.most_common():
        print("   ", n, ":", cs)
