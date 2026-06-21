import sys, os, json, random, time, collections, statistics
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get, post
BASE = "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/"
CHUNK=40000
# verify 40k works
mid="2M/PI/CPI/2012/0012M4ACPI1.px"
meta=get(BASE+mid,timeout=(10,60)).json()
v={x["code"]:x["values"] for x in meta["variables"]}
sel=[{"code":"Geolocation","selection":{"filter":"item","values":v["Geolocation"]}},  #101
     {"code":"Commodity Description","selection":{"filter":"item","values":v["Commodity Description"][:30]}}, #30
     {"code":"Year","selection":{"filter":"item","values":v["Year"][:13] if False else v["Year"]}}, #10
     {"code":"Period","selection":{"filter":"item","values":v["Period"][:1]}}] #1 ->101*30*10=30300
r=post(BASE+mid,json={"query":sel,"response":{"format":"json-stat2"}},timeout=(10,180))
print("40k-ish (30300) status:",r.status_code)

# recompute total requests with CHUNK over fresh sample
ents=list(json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/philippine-statistics-authority/assets/collect/entities/current.json")).keys())
random.seed(11); sample=random.sample(ents,60)
calls=collections.deque()
def thr():
    now=time.time()
    while calls and now-calls[0]>10: calls.popleft()
    if len(calls)>=8: time.sleep(max(10-(now-calls[0])+0.3,0))
    calls.append(time.time())
total_req=0; ncell=[]
for p in sample:
    thr()
    try: m=get(BASE+p,timeout=(10,60)).json()
    except Exception as e: print("err",p,e); continue
    c=1
    for vv in m.get("variables",[]): c*=len(vv.get("values") or [1])
    ncell.append(c); total_req += max(1, -(-c//CHUNK))
print("sampled",len(ncell),"median cells",statistics.median(ncell))
print("avg requests/table:",round(total_req/len(ncell),2))
print("EXTRAPOLATED total data-POSTs for 3049:",int(total_req/len(ncell)*3049))
print("plus 3049 metadata GETs; at ~1 req/s =>", round((total_req/len(ncell)*3049+3049)/3600,1),"hours")
