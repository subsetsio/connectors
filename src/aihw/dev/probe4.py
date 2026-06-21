from subsets_utils import get, transient_retry
import json, time
MYH="https://myhospitalsapi.aihw.gov.au/api/v1"
H={"Accept":"application/json"}

@transient_retry(attempts=6)
def page(code, top, skip):
    r=get(f"{MYH}/flat-data-extract/{code}", headers=H, params={"top":top,"skip":skip}, timeout=(10,180))
    r.raise_for_status()
    return r.json()["result"]["data"]

# find reliable top for MYH-ADM
for top in [200,100]:
    t=time.time()
    try:
        rows=page("MYH-ADM",top,0)
        print(f"MYH-ADM top={top}: {len(rows)} rows in {time.time()-t:.1f}s OK")
        break
    except Exception as e:
        print(f"top={top} ERR {type(e).__name__}")

# total rows per category at top=200
TOP=200
total=0; fr=None
for code in ['MYH-ADM','MYH-CANCER','MYH-CWS','MYH-ED','MYH-ED-TIME','MYH-ED-WAITS','MYH-ES','MYH-HH','MYH-LOS','MYH-RSI','MYH-SAB','MYH-SSI']:
    skip=0;n=0
    while True:
        rows=page(code,TOP,skip)
        if fr is None and rows: fr=rows[0]
        n+=len(rows)
        if len(rows)<TOP: break
        skip+=TOP
    print(f"  {code}: {n}")
    total+=n
print("TOTAL:",total)
print("keys:", sorted(fr.keys()))
