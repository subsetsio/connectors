import base64, json
from subsets_utils import get, post

HOST = "https://wabi-south-africa-north-a-primary-api.analysis.windows.net"
TOKEN = "eyJrIjoiZTQ3Njg5MDktNGNjMS00MTY0LWE1M2EtNGE1Y2FiMTlhZDc2IiwidCI6IjkzYWVkYmRjLWNjNjctNDY1Mi1hYTEyLWQyNTBhODc2YWU3OSIsImMiOjh9"
tok = json.loads(base64.b64decode(TOKEN + "==").decode()); rk = tok["k"]
H = {"X-PowerBI-ResourceKey": rk}
me = get(f"{HOST}/public/reports/{rk}/modelsAndExploration?preferReadOnlySession=true", headers=H, timeout=(10,60)).json()
model = me["models"][0]; modelId=model["id"]; dbName=model["dbName"]
expl = me["exploration"]; reportId=expl.get("reportId")
sec=expl["sections"][0]
best=None
for vc in sec["visualContainers"]:
    cfg=json.loads(vc.get("config","{}")); sv=cfg.get("singleVisual",{}); pq=sv.get("prototypeQuery")
    if pq and (best is None or len(pq["Select"])>len(best["Select"])): best=pq
pq=best; nsel=len(pq["Select"])
body={"version":"1.0.0","queries":[{"Query":{"Commands":[{"SemanticQueryDataShapeCommand":{
    "Query":pq,"Binding":{"Primary":{"Groupings":[{"Projections":list(range(nsel))}]},
    "DataReduction":{"DataVolume":4,"Primary":{"Window":{"Count":30000}}},"Version":1}}}]},
    "QueryId":"","ApplicationContext":{"DatasetId":dbName,"Sources":[{"ReportId":reportId}]}}],
    "cancelQueries":[],"modelId":modelId}
res=post(f"{HOST}/public/reports/querydata?synchronous=true",headers={**H,"Content-Type":"application/json;charset=UTF-8"},json=body,timeout=(10,120)).json()
data=res["results"][0]["result"]["data"]
desc=data["descriptor"]["Select"]
names=[d.get("Name") for d in desc]
ds=data["dsr"]["DS"][0]
dm=ds["PH"][0]["DM0"]
valuedicts=ds.get("ValueDicts",{})

# determine column count from first S row
S=dm[0]["S"]; ncols=len(S)
print("ncols from S", ncols, "nsel", nsel)
def popcount(x): return bin(x).count("1")
for idx in range(1,4):
    r=dm[idx]; R=r.get("R",0); O=r.get("Ø",0); C=r.get("C",[])
    print(f"row{idx}: lenC={len(C)} popR={popcount(R)} popO={popcount(O)} ncols-lenC={ncols-len(C)}")

def decode(dm, ncols):
    rows=[]; prev=[None]*ncols
    for r in dm:
        if "S" in r:  # header
            continue
        C=r.get("C",[]); R=r.get("R",0); O=r.get("Ø",0)
        row=[]; ci=0
        for i in range(ncols):
            bit=1<<i
            if R & bit: row.append(prev[i])
            elif O & bit: row.append(None)
            else:
                v=C[ci]; ci+=1; row.append(v)
        assert ci==len(C), f"consumed {ci} of {len(C)}"
        prev=row; rows.append(row)
    return rows
rows=decode(dm,ncols)
print("decoded rows", len(rows))
print("clean names:", names[:5])
import datetime
print("first row time", datetime.datetime.utcfromtimestamp(rows[0][0]/1000), "->", datetime.datetime.utcfromtimestamp(rows[-1][0]/1000))
print("row0 sample vals:", rows[0][:6])
print("row1 sample vals:", rows[1][:6])
# check time monotonic hourly
ts=[r[0] for r in rows]
difs={(ts[i+1]-ts[i]) for i in range(len(ts)-1)}
print("time deltas (ms):", difs)
