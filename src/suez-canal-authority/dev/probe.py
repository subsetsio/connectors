import json, gzip
from subsets_utils import get, post

BASE = "https://wabi-europe-north-b-api.analysis.windows.net/public/reports"
KEY = "f394fa83-f56e-4ff5-8877-a2c015ca9cfe"  # quarterly by ship type

def _json(resp):
    return resp.json()

h = {"X-PowerBI-ResourceKey": KEY}
me = _json(get(f"{BASE}/{KEY}/modelsAndExploration?preferReadOnlySession=true", headers=h, timeout=60))
model = me["models"][0]; expl = me["exploration"]
mid, db, rid = model["id"], model["dbName"], expl["reportId"]
print("model:", model.get("displayName"), "| mid", mid, "rid", rid, "db", db)

cs = _json(post(f"{BASE}/conceptualschema", headers=h, json={"modelIds":[mid],"userPreferredLocale":"en-US"}, timeout=60))
ent = [e for s in cs["schemas"] for e in s["schema"]["Entities"] if not e.get("Private")][0]
entity = ent["Name"]
cols = [(p["Name"], p.get("DataType")) for p in ent["Properties"]]
print("entity:", entity)
print("cols:", cols)

# Select ALL columns as plain Column projections (no aggregation)
sel = [{"Column":{"Expression":{"SourceRef":{"Source":"r"}},"Property":c},"Name":f"{entity}.{c}"} for c,_ in cols]
q = {"Commands":[{"SemanticQueryDataShapeCommand":{
    "Query":{"Version":2,"From":[{"Name":"r","Entity":entity,"Type":0}],"Select":sel},
    "Binding":{"Primary":{"Groupings":[{"Projections":list(range(len(sel)))}]},
               "DataReduction":{"DataVolume":4,"Primary":{"Window":{"Count":30000}}},"Version":1}}}]}
body = {"version":"1.0.0","queries":[{"Query":q,"QueryId":"","ApplicationContext":{"DatasetId":db,"Sources":[{"ReportId":rid}]}}],"cancelQueries":[],"modelId":mid}
out = _json(post(f"{BASE}/querydata?synchronous=true", headers=h, json=body, timeout=90))
data = out["results"][0]["result"]["data"]
dsr = data["dsr"]
print("\n=== descriptor (data.descriptor.Select) ===")
desc = data.get("descriptor",{})
print(json.dumps(desc, indent=1)[:1500])
ds = dsr["DS"][0]
print("\n=== DS[0] keys ===", list(ds.keys()))
print("ValueDicts keys:", list(ds.get("ValueDicts",{}).keys()))
for k,v in ds.get("ValueDicts",{}).items():
    print("  ",k, "->", v[:6], f"(n={len(v)})")
print("\n=== DS[0].S (column descriptor) ===")
print(json.dumps(ds.get("S"), indent=1)[:1500])
ph = ds["PH"][0]["DM0"]
print("\n=== first 8 DM0 rows (raw) ===")
for r in ph[:8]:
    print(r)
print("total rows:", len(ph))
