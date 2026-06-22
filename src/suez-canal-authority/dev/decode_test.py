import json
from subsets_utils import get, post
BASE="https://wabi-europe-north-b-api.analysis.windows.net/public/reports"

def fetch_report(key):
    h={"X-PowerBI-ResourceKey":key}
    me=get(f"{BASE}/{key}/modelsAndExploration?preferReadOnlySession=true",headers=h,timeout=60).json()
    model=me["models"][0]; expl=me["exploration"]
    mid,db,rid=model["id"],model["dbName"],expl["reportId"]
    cs=post(f"{BASE}/conceptualschema",headers=h,json={"modelIds":[mid],"userPreferredLocale":"en-US"},timeout=60).json()
    ent=[e for s in cs["schemas"] for e in s["schema"]["Entities"] if not e.get("Private")][0]
    entity=ent["Name"]; props=[p["Name"] for p in ent["Properties"]]
    sel=[{"Column":{"Expression":{"SourceRef":{"Source":"r"}},"Property":c},"Name":f"{entity}.{c}"} for c in props]
    q={"Commands":[{"SemanticQueryDataShapeCommand":{"Query":{"Version":2,"From":[{"Name":"r","Entity":entity,"Type":0}],"Select":sel},"Binding":{"Primary":{"Groupings":[{"Projections":list(range(len(sel)))}]},"DataReduction":{"DataVolume":4,"Primary":{"Window":{"Count":30000}}},"Version":1}}}]}
    body={"version":"1.0.0","queries":[{"Query":q,"QueryId":"","ApplicationContext":{"DatasetId":db,"Sources":[{"ReportId":rid}]}}],"cancelQueries":[],"modelId":mid}
    out=post(f"{BASE}/querydata?synchronous=true",headers=h,json=body,timeout=90).json()
    return out["results"][0]["result"]["data"], entity, props

def decode(data):
    ds=data["dsr"]["DS"][0]
    vd=ds.get("ValueDicts",{})
    dm0=ds["PH"][0]["DM0"]
    S=dm0[0]["S"]
    ncols=len(S)
    # Gn -> property name from descriptor.Select
    gn2prop={}
    for e in data["descriptor"]["Select"]:
        gk=e.get("GroupKeys")
        prop = gk[0]["Source"]["Property"] if gk else e.get("Name","").split(".")[-1]
        gn2prop[e["Value"]]=prop
    colnames=[gn2prop.get(s["N"], s["N"]) for s in S]
    dicts=[s.get("DN") for s in S]
    prev=[None]*ncols
    rows=[]
    for item in dm0:
        C=item.get("C",[]); R=item.get("R",0); O=item.get("Ø",0)
        ci=0; row=[None]*ncols
        for i in range(ncols):
            if O & (1<<i): row[i]=None
            elif R & (1<<i): row[i]=prev[i]
            else: row[i]=C[ci]; ci+=1
        prev=list(row)
        # resolve dict columns
        outrow={}
        for i in range(ncols):
            v=row[i]
            if dicts[i] is not None and isinstance(v,int):
                v=vd[dicts[i]][v]
            outrow[colnames[i]]=v
        rows.append(outrow)
    return colnames, rows

data,entity,props=fetch_report("f394fa83-f56e-4ff5-8877-a2c015ca9cfe")
cols,rows=decode(data)
print("entity:",entity)
print("schema props:",props)
print("decoded colnames:",cols)
print("nrows:",len(rows))
for r in rows[:6]: print(r)
print("...")
import collections
print("distinct years:", sorted(set(r.get("year") for r in rows))[:30])
print("distinct CategoryName_en:", sorted(set(r.get("CategoryName_en") for r in rows)))
print("distinct Port:", sorted(set(str(r.get("Port")) for r in rows)))
