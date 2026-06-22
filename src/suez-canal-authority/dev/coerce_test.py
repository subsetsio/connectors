import json
from subsets_utils import get, post
BASE="https://wabi-europe-north-b-api.analysis.windows.net/public/reports"
def fetch_report(key):
    h={"X-PowerBI-ResourceKey":key}
    me=get(f"{BASE}/{key}/modelsAndExploration?preferReadOnlySession=true",headers=h,timeout=60).json()
    model=me["models"][0]; expl=me["exploration"]; mid,db,rid=model["id"],model["dbName"],expl["reportId"]
    cs=post(f"{BASE}/conceptualschema",headers=h,json={"modelIds":[mid],"userPreferredLocale":"en-US"},timeout=60).json()
    ent=[e for s in cs["schemas"] for e in s["schema"]["Entities"] if not e.get("Private")][0]
    entity=ent["Name"]; props=[p["Name"] for p in ent["Properties"]]
    sel=[{"Column":{"Expression":{"SourceRef":{"Source":"r"}},"Property":c},"Name":f"{entity}.{c}"} for c in props]
    q={"Commands":[{"SemanticQueryDataShapeCommand":{"Query":{"Version":2,"From":[{"Name":"r","Entity":entity,"Type":0}],"Select":sel},"Binding":{"Primary":{"Groupings":[{"Projections":list(range(len(sel)))}]},"DataReduction":{"DataVolume":4,"Primary":{"Window":{"Count":30000}}},"Version":1}}}]}
    body={"version":"1.0.0","queries":[{"Query":q,"QueryId":"","ApplicationContext":{"DatasetId":db,"Sources":[{"ReportId":rid}]}}],"cancelQueries":[],"modelId":mid}
    return post(f"{BASE}/querydata?synchronous=true",headers=h,json=body,timeout=90).json()["results"][0]["result"]["data"]
def coerce(v,is_dict):
    if v is None or is_dict: return v
    if isinstance(v,(int,float)): return v
    s=str(v).strip()
    try:
        f=float(s); return int(f) if f.is_integer() else f
    except ValueError: return s
def decode(data):
    ds=data["dsr"]["DS"][0]; vd=ds.get("ValueDicts",{}); dm0=ds["PH"][0]["DM0"]
    if not dm0: return []
    S=dm0[0]["S"]; ncols=len(S)
    gn2={e["Value"]:(e["GroupKeys"][0]["Source"]["Property"] if e.get("GroupKeys") else e.get("Name","").split(".")[-1]) for e in data["descriptor"]["Select"]}
    names=[gn2.get(s["N"],s["N"]) for s in S]; dicts=[s.get("DN") for s in S]
    prev=[None]*ncols; rows=[]
    for item in dm0:
        C=item.get("C",[]);R=item.get("R",0);O=item.get("Ø",0);ci=0;row=[None]*ncols
        for i in range(ncols):
            if O&(1<<i):row[i]=None
            elif R&(1<<i):row[i]=prev[i]
            else:row[i]=C[ci];ci+=1
        prev=list(row)
        out={}
        for i in range(ncols):
            v=row[i]
            if dicts[i] is not None and isinstance(v,int): v=vd[dicts[i]][v]
            out[names[i]]=coerce(v, dicts[i] is not None)
        rows.append(out)
    return rows
import collections
for eid,key in [("02","cfd839a0-d4ac-4df7-a6e7-308bf576098b"),("03","173bc878-0a20-4bc1-b738-08d2de20719e")]:
    rows=decode(fetch_report(key))
    print(f"\n{eid}: {len(rows)} rows")
    types=collections.defaultdict(set)
    for r in rows:
        for k,v in r.items(): types[k].add(type(v).__name__)
    for k,t in types.items(): print(f"   {k!r}: {sorted(t)}")
    print("   sample:",rows[0])
