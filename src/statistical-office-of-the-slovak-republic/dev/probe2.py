from subsets_utils import get, transient_retry
import json, math

@transient_retry()
def gj(url):
    r = get(url, timeout=(30,180)); r.raise_for_status(); return r.json()

d = gj("https://data.statistics.sk/api/v2/dataset/as1001rs/all/all/all?lang=en")
for dim in d['id']:
    obj = d['dimension'][dim]
    cat = obj.get('category',{})
    idx = cat.get('index'); lab = cat.get('label')
    print(f"DIM {dim}: label={obj.get('label')!r}")
    print(f"   index type={type(idx).__name__} sample={list(idx.items())[:3] if isinstance(idx,dict) else (idx[:3] if idx else None)}")
    print(f"   label sample={list(lab.items())[:3] if isinstance(lab,dict) else None}")

col = gj("https://data.statistics.sk/api/v2/collection?lang=en")
items = col['link']['item']
items_sorted = sorted(items, key=lambda it: len(it.get('dimension',{})), reverse=True)
for it in items_sorted[:4]:
    cube=it['href'].split('/dataset/')[1].split('/')[0]
    print(f"BIG {cube} ndim={len(it['dimension'])} {it['label']!r}")
