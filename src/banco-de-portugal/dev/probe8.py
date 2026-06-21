import json, math
from subsets_utils import get
BASE="https://bpstat.bportugal.pt/data/v1"
ds="08ea9a8e70896fd8c1fd3b99d71c7dc4"
url=f"{BASE}/domains/3/datasets/{ds}/?lang=EN"
# find max page_size
for ps in [1000, 500, 200, 100]:
    r=get(url, params={"page":1,"page_size":ps}, timeout=(10,120))
    print(f"page_size={ps}: {r.status_code} {r.text[:120] if r.status_code!=200 else 'OK ext='+str(len(r.json()['extension']['series']))}")
print("---default + link/header inspection---")
r=get(url, params={"page":1}, timeout=(10,120))
d=r.json()
print("default ext series:", len(d["extension"]["series"]), "size:", d["size"])
print("top keys:", list(d.keys()))
print("link:", json.dumps(d.get("link",{}))[:400])
print("headers count-ish:", {k:v for k,v in r.headers.items() if k.lower() in ('x-total-count','x-total-pages','link','content-range')})
# walk pages until error/empty at page_size 100
print("---walk pages ps=100---")
total=0; p=1
while True:
    r=get(url, params={"page":p,"page_size":100}, timeout=(10,120))
    if r.status_code!=200:
        print("stop at page",p,"status",r.status_code, r.text[:80]); break
    d=r.json()
    n=len(d["extension"]["series"])
    total+=n
    print(f"page {p}: {n} series, cumulative {total}")
    if n==0: break
    p+=1
    if p>15: print("safety stop"); break
print("TOTAL series collected:", total, "expected 917")
