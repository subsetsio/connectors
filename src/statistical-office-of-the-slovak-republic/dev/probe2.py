from subsets_utils import get
import json, math

# dimension structure
r = get("https://data.statistics.sk/api/v2/dataset/as1001rs/all/all/all?lang=en", timeout=(10,120))
d = r.json()
for dim in d['id']:
    obj = d['dimension'][dim]
    cat = obj.get('category',{})
    idx = cat.get('index')
    lab = cat.get('label')
    print(f"DIM {dim}: label={obj.get('label')!r} note={obj.get('note')}")
    print(f"   index type={type(idx).__name__} sample={list(idx.items())[:3] if isinstance(idx,dict) else idx[:3] if idx else None}")
    print(f"   label sample={list(lab.items())[:3] if isinstance(lab,dict) else None}")

# Find a large cube. Check collection for dimension counts, then probe biggest.
col = get("https://data.statistics.sk/api/v2/collection?lang=en", timeout=(10,120)).json()
items = col['link']['item']
# pick the one with most dimensions
items_sorted = sorted(items, key=lambda it: len(it.get('dimension',{})), reverse=True)
for it in items_sorted[:3]:
    href=it['href']; cube=href.split('/dataset/')[1].split('/')[0]
    ndim=len(it['dimension'])
    print(f"\nBIG cube {cube} ndim={ndim} label={it['label']!r}")
