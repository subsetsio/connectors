import csv, io, json, concurrent.futures as cf
from subsets_utils import get

union = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/instituto-nacional-de-estad-sticas/work/entity_union.json"))
ids = union if isinstance(union, list) else list(union)
print("union size", len(ids))

def check(did):
    url = f"https://sdmx.ine.gob.cl/rest/data/CL01,{did},1.0?format=csv&lastNObservations=1"
    try:
        r = get(url, headers={"Accept":"application/vnd.sdmx.data+csv"}, timeout=(10,120))
        if r.status_code != 200:
            return (did, r.status_code, 0)
        rows = list(csv.reader(io.StringIO(r.text)))
        return (did, 200, max(0, len(rows)-1))
    except Exception as e:
        return (did, "ERR", str(e)[:60])

bad=[]; empty=[]; ok=0
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    for did, st, n in ex.map(check, ids):
        if st != 200: bad.append((did, st, n))
        elif n == 0: empty.append(did)
        else: ok+=1
print("ok(>=1 row):", ok)
print("empty(200, 0 rows):", len(empty), empty)
print("non-200:", len(bad))
for b in bad: print("  ", b)
