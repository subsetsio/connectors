from subsets_utils import get, transient_retry
import json
@transient_retry(attempts=8, min_wait=2, max_wait=30)
def gj(url):
    r = get(url, timeout=(60,180)); r.raise_for_status(); return r.json()
d = gj("https://data.statistics.sk/api/v2/dataset/as1001rs/all/all/all?lang=en")
for dim in d['id']:
    o=d['dimension'][dim]; cat=o.get('category',{})
    idx=cat.get('index'); lab=cat.get('label')
    print(f"DIM {dim}: label={o.get('label')!r}")
    print(f"   idx={list(idx.items())[:2] if isinstance(idx,dict) else (idx[:2] if idx else None)}")
    print(f"   lab={list(lab.items())[:2] if isinstance(lab,dict) else None}")
