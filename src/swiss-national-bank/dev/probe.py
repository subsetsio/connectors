import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
import json
from subsets_utils import get

union = json.load(open('/Users/nathansnellaert/Documents/hardened/data/sources/swiss-national-bank/work/entity_union.json'))
wh = [c for c in union if '@' in c]
tp = [c for c in union if '@' not in c]
print(f"union={len(union)} warehouse={len(wh)} topic={len(tp)}")

# sample: a few topic + a few warehouse spanning depths
sample = (tp[:3] if tp else []) + [wh[0], wh[4], wh[len(wh)//2], wh[-1]]
def url_for(cid):
    if '@' in cid:
        return f"https://data.snb.ch/api/warehouse/cube/{cid.replace('@','.')}/data/json/en"
    return f"https://data.snb.ch/api/cube/{cid}/data/json/en"

for cid in sample:
    try:
        r = get(url_for(cid), timeout=(10,120))
        r.raise_for_status()
        d = r.json()
        ts = d.get('timeseries', [])
        nseries = len(ts)
        nvals = sum(len(s.get('values',[])) for s in ts)
        nonnull = sum(1 for s in ts for v in s.get('values',[]) if v.get('value') is not None)
        s0 = ts[0] if ts else {}
        print(f"\n{cid}: series={nseries} totvals={nvals} nonnull={nonnull}")
        if s0:
            print("  header:", json.dumps(s0.get('header')))
            print("  metadata:", json.dumps(s0.get('metadata')))
            print("  sample vals:", json.dumps(s0.get('values',[])[:2]))
    except Exception as e:
        print(f"\n{cid}: ERROR {type(e).__name__} {e}")
