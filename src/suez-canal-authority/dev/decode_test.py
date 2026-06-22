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

print("\n\n========== ALL 7 REPORTS ==========")
KEYMAP={
 "01-monthly-number-net-ton-by-ship-type":"37989a27-9212-47b5-af4a-4e24459656ce",
 "02-fiscal-year-statistical":"cfd839a0-d4ac-4df7-a6e7-308bf576098b",
 "03-yearly-statistics":"173bc878-0a20-4bc1-b738-08d2de20719e",
 "04-yearly-cargo-ton-by-direction":"a9b8cc80-3266-4a27-bb9d-50ccb99ba5d6",
 "05-yealy-cargo-ton-by-region":"f394fa83-f56e-4ff5-8877-a2c015ca9cfe",
 "06-yealy-cargo-ton-by-region-cont":"620624d7-ba78-4a4b-a04a-3bb4d7f69b95",
 "07-yearly-cargo-ton-by-cargo-type":"4421f780-4bb4-47ac-8e7d-aba8b30360e6",
}
for eid,key in KEYMAP.items():
    try:
        data,entity,props=fetch_report(key)
        cols,rows=decode(data)
        print(f"\n## {eid}  entity={entity} nrows={len(rows)}")
        print("   cols:",cols)
        print("   sample:",rows[0] if rows else None)
        # year-ish ranges
        for yc in ("year","Year","Fiscal Year"):
            if rows and yc in rows[0]:
                ys=sorted(set(r[yc] for r in rows if r[yc] is not None))
                print(f"   {yc} range:",ys[0],"..",ys[-1],f"({len(ys)})")
    except Exception as e:
        print(eid,"ERR",type(e).__name__,str(e)[:160])

print("\n\n========== GRAIN CHECKS ==========")
def grain(eid,key,dims):
    data,entity,props=fetch_report(key)
    cols,rows=decode(data)
    seen={}
    for r in rows:
        k=tuple(r.get(d) for d in dims)
        seen.setdefault(k,0); seen[k]+=1
    dups={k:v for k,v in seen.items() if v>1}
    print(f"{eid}: {len(rows)} rows, key {dims} -> {len(seen)} distinct, {len(dups)} dup-keys")
    if dups: print("   example dup:",list(dups.items())[:2])
grain("01","37989a27-9212-47b5-af4a-4e24459656ce",["year","Month","Ship Type","Direction","State"])
grain("05","f394fa83-f56e-4ff5-8877-a2c015ca9cfe",["year","Quarter","CategoryName_en","Port"])
grain("06","620624d7-ba78-4a4b-a04a-3bb4d7f69b95",["year","Region","Direction","Terminal"])
grain("07","4421f780-4bb4-47ac-8e7d-aba8b30360e6",["Year","CargoType","Goods","Direction"])
grain("04","a9b8cc80-3266-4a27-bb9d-50ccb99ba5d6",["Year","Direction"])
grain("03","173bc878-0a20-4bc1-b738-08d2de20719e",["Year"])
grain("02","cfd839a0-d4ac-4df7-a6e7-308bf576098b",["Fiscal Year"])

print("\n\n========== DUP ROW INSPECTION ==========")
def show_dups(eid,key,dims,target):
    data,entity,props=fetch_report(key)
    cols,rows=decode(data)
    matches=[r for r in rows if tuple(r.get(d) for d in dims)==target]
    print(f"\n{eid} rows where {dims}=={target}:")
    for r in matches: print("  ",r)
show_dups("05","f394fa83-f56e-4ff5-8877-a2c015ca9cfe",["year","Quarter","CategoryName_en","Port"],(2014,3,'General Cargo','S/N'))
show_dups("06","620624d7-ba78-4a4b-a04a-3bb4d7f69b95",["year","Region","Direction","Terminal"],(2011,'America','North / South','Origin'))
# 07
data,entity,props=fetch_report("4421f780-4bb4-47ac-8e7d-aba8b30360e6")
cols,rows=decode(data)
ms=[r for r in rows if (r.get("Year"),r.get("CargoType"),r.get("Goods"),r.get("Direction"))==(2011,'Cereals','Other Goods','South / North')]
print("\n07 rows where (2011,Cereals,Other Goods,South/North):")
for r in ms[:12]: print("  ",r)
# check finer grains
def grain2(eid,key,dims):
    data,entity,props=fetch_report(key); cols,rows=decode(data)
    seen={}
    for r in rows:
        k=tuple(r.get(d) for d in dims); seen[k]=seen.get(k,0)+1
    dups=sum(1 for v in seen.values() if v>1)
    print(f"{eid}: key {dims} -> {len(seen)} distinct of {len(rows)} rows, {dups} dup-keys")
print()
grain2("06","620624d7-ba78-4a4b-a04a-3bb4d7f69b95",["year","Region_Code","Direction","Terminal"])
grain2("07","4421f780-4bb4-47ac-8e7d-aba8b30360e6",["Year","CargoType","Goods","Direction","Custom Order"])
grain2("07","4421f780-4bb4-47ac-8e7d-aba8b30360e6",["Year","CargoType","Goods","Direction","Cargo Type"])
grain2("05","f394fa83-f56e-4ff5-8877-a2c015ca9cfe",["year","Quarter","CategoryName_en","Port","prt"])
grain2("05","f394fa83-f56e-4ff5-8877-a2c015ca9cfe",["year","Quarter","CategoryName_en","Port","vcode"])
