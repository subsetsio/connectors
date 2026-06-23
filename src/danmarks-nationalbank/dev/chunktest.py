import json
from subsets_utils import get, get_client, transient_retry
API = "https://api.statbank.dk/v1"
TARGET_CELLS = 250_000
MAX_PERIODS = 2000

@transient_retry()
def info(tid):
    r = get(f"{API}/tableinfo/{tid}", params={"format":"JSON"}, timeout=(10,120))
    r.raise_for_status(); return r.json()

@transient_retry()
def fetch_slice(body, time_codes):
    rows=[]
    with get_client().stream("POST", f"{API}/data", json=body, timeout=(10,600)) as r:
        r.raise_for_status()
        lines=r.iter_lines()
        header=next(lines,None)
        if header is None: return rows
        keys=["value" if c.strip().upper()=="INDHOLD" else "time" if c.strip().upper() in time_codes else c.strip().lower() for c in header.split(";")]
        nc=len(keys)
        for line in lines:
            if not line: continue
            p=line.split(";")
            if len(p)!=nc: continue
            rows.append({keys[i]:p[i] for i in range(nc)})
    return rows

def run(tid):
    inf=info(tid)
    variables=inf["variables"]
    varcodes=[v["id"] for v in variables]
    tv=next((v for v in variables if v.get("time")),None)
    tcs={tv["id"].upper()} if tv else set()
    pids=[x["id"] for x in tv["values"]]
    other=1
    for v in variables:
        if not v.get("time"): other*=max(1,len(v["values"]))
    per=min(max(1,TARGET_CELLS//max(1,other)),MAX_PERIODS)
    non_time=[c for c in varcodes if c!=tv["id"]]
    total=0; nreq=0; sample=None
    for i in range(0,len(pids),per):
        chunk=pids[i:i+per]
        body={"table":tid,"lang":"en","format":"BULK","variables":[{"code":c,"values":["*"]} for c in non_time]+[{"code":tv["id"],"values":chunk}]}
        rows=fetch_slice(body,tcs); nreq+=1; total+=len(rows)
        if sample is None and rows: sample=rows[0]
    print(f"{tid}: periods={len(pids)} per_chunk={per} requests={nreq} rows={total}", flush=True)
    print(f"   sample={sample}", flush=True)

for tid in ["DNVPDKR2","DNVPDKF","DNSUBOH","DNIFHVEM"]:
    try: run(tid)
    except Exception as e: print(f"{tid}: FAIL {type(e).__name__} {str(e)[:140]}", flush=True)
