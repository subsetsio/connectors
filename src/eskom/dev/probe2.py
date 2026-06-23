import base64, json
from subsets_utils import get, post

HOST = "https://wabi-south-africa-north-a-primary-api.analysis.windows.net"
TOKEN = "eyJrIjoiZTQ3Njg5MDktNGNjMS00MTY0LWE1M2EtNGE1Y2FiMTlhZDc2IiwidCI6IjkzYWVkYmRjLWNjNjctNDY1Mi1hYTEyLWQyNTBhODc2YWU3OSIsImMiOjh9"
tok = json.loads(base64.b64decode(TOKEN + "==").decode()); rk = tok["k"]
H = {"X-PowerBI-ResourceKey": rk}

me = get(f"{HOST}/public/reports/{rk}/modelsAndExploration?preferReadOnlySession=true", headers=H, timeout=(10,60)).json()
model = me["models"][0]
modelId = model["id"]; dbName = model["dbName"]
expl = me["exploration"]; reportId = expl.get("reportId")
sec = expl["sections"][0]
# pick the visual with the most Select columns (the data chart)
best=None
for vc in sec["visualContainers"]:
    cfg = json.loads(vc.get("config","{}")); sv = cfg.get("singleVisual",{})
    pq = sv.get("prototypeQuery")
    if pq and (best is None or len(pq["Select"])>len(best[1]["Select"])):
        best=(sv.get("visualType"), pq)
vtype, pq = best
nsel = len(pq["Select"])
print("visual", vtype, "select cols", nsel, "modelId", modelId, "reportId", reportId)
print("columns:", [s.get("Name") for s in pq["Select"]][:6], "...")

body = {
  "version":"1.0.0",
  "queries":[{
    "Query":{"Commands":[{"SemanticQueryDataShapeCommand":{
        "Query": pq,
        "Binding":{"Primary":{"Groupings":[{"Projections":list(range(nsel))}]},
                   "DataReduction":{"DataVolume":4,"Primary":{"Window":{"Count":30000}}},
                   "Version":1}
    }}]},
    "QueryId":"",
    "ApplicationContext":{"DatasetId":dbName,"Sources":[{"ReportId":reportId}]}
  }],
  "cancelQueries":[],
  "modelId":modelId
}
r = post(f"{HOST}/public/reports/querydata?synchronous=true", headers={**H,"Content-Type":"application/json;charset=UTF-8"}, json=body, timeout=(10,120))
print("querydata", r.status_code, "bytes", len(r.content))
if r.status_code!=200:
    print(r.text[:800]); raise SystemExit
res = r.json()
dsr = res["results"][0]["result"]["data"]["dsr"]
print("dsr keys", list(dsr.keys()))
ds = dsr["DS"][0]
print("DS keys", list(ds.keys()))
print("has ValueDicts:", "ValueDicts" in ds, list(ds.get("ValueDicts",{}).keys())[:8])
ph = ds["PH"][0]
print("PH keys", list(ph.keys()))
dm = ph[list(ph.keys())[0]]
print("n datarows", len(dm))
print("first 3 rows raw:")
for row in dm[:3]:
    print(json.dumps(row)[:300])
print("last row raw:", json.dumps(dm[-1])[:300])
# descriptor
desc = res["results"][0]["result"]["data"]["descriptor"]["Select"]
print("descriptor names:", [d.get("Name") for d in desc][:6])
