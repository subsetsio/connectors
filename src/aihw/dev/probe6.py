from subsets_utils import get
import json,time
MYH="https://myhospitalsapi.aihw.gov.au/api/v1"
H={"Accept":"application/json"}
for path in ["measure-downloads/myh-adm","measure-downloads/across-reporting-units/myh-adm"]:
    t=time.time()
    try:
        r=get(f"{MYH}/{path}", headers=H, timeout=(10,180))
        ct=r.headers.get("content-type")
        body=r.content
        print(path,"status",r.status_code,"ct",ct,"bytes",len(body),"in",round(time.time()-t,1),"s")
        try:
            d=r.json()
            res=d.get("result", d)
            print("  json keys/sample:", json.dumps(res)[:400])
        except Exception:
            print("  text head:", body[:300])
    except Exception as e:
        print(path,"ERR",type(e).__name__,e)
