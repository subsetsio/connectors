import sys, os, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import nodes.seer as m
from subsets_utils import load_raw_ndjson
sid="seer-incidence-and-mortality-comparison-recent-rates"
m.fetch_one(sid)
rows=load_raw_ndjson(sid)
cols=sorted(rows[0].keys())
print(sid, "cols:", cols)
print("has 'site' col:", 'site' in cols)
sites={r.get('site') for r in rows}
print("distinct site values:", list(sites)[:5], "count:", len(sites))
# check duplication on non-site key
from collections import Counter
key=Counter(tuple(r.get(c) for c in cols if c!='site') for r in rows)
dups=sum(1 for v in key.values() if v>1)
print("rows:",len(rows),"distinct non-site keys:",len(key),"keys-with-dups:",dups)
