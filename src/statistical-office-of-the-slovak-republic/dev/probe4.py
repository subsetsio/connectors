from subsets_utils import get, transient_retry
import json, math
@transient_retry(attempts=10, min_wait=1, max_wait=20)
def gj(url):
    r = get(url, timeout=(60,180)); r.raise_for_status(); return r.json()

# (a) category structure on small cube
d = gj("https://data.statistics.sk/api/v2/dataset/as1001rs/all/all/all?lang=en")
print("ROLE:", d.get('role'))
for dim in d['id']:
    o=d['dimension'][dim]; cat=o.get('category',{})
    idx=cat.get('index'); lab=cat.get('label')
    print(f"DIM {dim}: label={o.get('label')!r} idxtype={type(idx).__name__}",
          "idx2=", (list(idx.items())[:2] if isinstance(idx,dict) else (idx[:2] if idx else None)),
          "lab2=", (list(lab.items())[:2] if isinstance(lab,dict) else None))
print("value0..3:", d['value'][:4], "valtype:", type(d['value']).__name__, "len:", len(d['value']) if isinstance(d['value'],(list,dict)) else None)

# (b) cap behavior: pick the biggest cube by product of dimension sizes via /dimension calls
col = gj("https://data.statistics.sk/api/v2/collection?lang=en")
items = col['link']['item']
# heuristic: cubes likely big -> many dims. test om7055rr (6 dims, demographic balance by district)
for cube in ["om7055rr"]:
    it = next(x for x in items if x['href'].split('/dataset/')[1].split('/')[0]==cube)
    dims = list(it['dimension'].keys())
    sizes=[]
    for dm in dims:
        dd = gj(f"https://data.statistics.sk/api/v2/dimension/{cube}/{dm}?lang=en")
        # json-stat class dimension: category.index
        cidx = dd.get('category',{}).get('index')
        n = len(cidx) if cidx else None
        sizes.append(n)
    print(f"\nCUBE {cube} dims={dims} sizes={sizes} product={math.prod([s for s in sizes if s])}")
    # request all/all... and see size vs value length
    sel="/".join(["all"]*len(dims))
    big = gj(f"https://data.statistics.sk/api/v2/dataset/{cube}/{sel}?lang=en")
    sz=big.get('size'); val=big.get('value')
    print("returned size:", sz, "prod:", math.prod(sz), "value_len:", len(val) if isinstance(val,(list,dict)) else None,
          "value_is_dict:", isinstance(val,dict))
