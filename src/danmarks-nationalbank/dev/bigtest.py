import json, gzip, tempfile, os
from subsets_utils import get, get_client, transient_retry
API = "https://api.statbank.dk/v1"

def info(tid):
    r = get(f"{API}/tableinfo/{tid}", params={"format":"JSON"}, timeout=(10,120))
    r.raise_for_status(); return r.json()

@transient_retry()
def stream(tid, body, time_codes):
    tmp = tempfile.NamedTemporaryFile(suffix=".ndjson.gz", delete=False).name
    n=0
    with get_client().stream("POST", f"{API}/data", json=body, timeout=(10,600)) as r:
        r.raise_for_status()
        lines = r.iter_lines()
        cols=[c.strip() for c in next(lines).split(";")]
        keys=["value" if c.upper()=="INDHOLD" else "time" if c.upper() in time_codes else c.lower() for c in cols]
        nc=len(keys)
        with gzip.open(tmp,"wt",encoding="utf-8") as f:
            for line in lines:
                if not line: continue
                p=line.split(";")
                if len(p)!=nc: continue
                f.write(json.dumps({keys[i]:p[i] for i in range(nc)},separators=(",",":"))+"\n"); n+=1
    os.unlink(tmp)
    return n

for tid in ["DNVPDKR2","DNIFHVEM","DNIFINVE"]:
    inf=info(tid)
    vc=[v["id"] for v in inf["variables"]]
    tc={v["id"].upper() for v in inf["variables"] if v.get("time")}
    body={"table":tid,"lang":"en","format":"BULK","variables":[{"code":c,"values":["*"]} for c in vc]}
    try:
        n=stream(tid,body,tc)
        print(f"{tid}: OK rows={n}", flush=True)
    except Exception as e:
        print(f"{tid}: FAIL {type(e).__name__} {str(e)[:120]}", flush=True)
