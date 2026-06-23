import json, datetime
from subsets_utils import get, post
HOST="https://wabi-south-africa-north-a-primary-api.analysis.windows.net"
def mae(rk): return get(f"{HOST}/public/reports/{rk}/modelsAndExploration?preferReadOnlySession=true",headers={"X-PowerBI-ResourceKey":rk},timeout=(10,60)).json()
def biggest(rk):
    me=mae(rk); vs=[]
    for sec in me["exploration"]["sections"]:
        for vc in sec.get("visualContainers",[]):
            pq=json.loads(vc.get("config","{}")).get("singleVisual",{}).get("prototypeQuery")
            if pq and any('Aggregation' in s for s in pq['Select']) and any('Aggregation' not in s for s in pq['Select']): vs.append(pq)
    return me,max(vs,key=lambda p:len(p['Select']))
def run(rk):
    me,pq=biggest(rk); model=me["models"][0]; n=len(pq["Select"])
    body={"version":"1.0.0","queries":[{"Query":{"Commands":[{"SemanticQueryDataShapeCommand":{"Query":pq,
      "Binding":{"Primary":{"Groupings":[{"Projections":list(range(n))}]},"DataReduction":{"DataVolume":4,"Primary":{"Window":{"Count":50000}}},"Version":1}}}]},
      "QueryId":"","ApplicationContext":{"DatasetId":model["dbName"],"Sources":[{"ReportId":me["exploration"].get("reportId")}]}}],"cancelQueries":[],"modelId":model["id"]}
    return post(f"{HOST}/public/reports/querydata?synchronous=true",headers={"X-PowerBI-ResourceKey":rk,"Content-Type":"application/json"},json=body,timeout=(10,120)).json()["results"][0]["result"]["data"]
def decode(ds):
    dm=ds["PH"][0]["DM0"]; S=next(x["S"] for x in dm if "S" in x); n=len(S)
    dicts=ds.get("ValueDicts",{}); DN=[s.get("DN") for s in S]; T=[s.get("T") for s in S]; N=[s["N"] for s in S]
    rows=[]; prev=[None]*n
    for x in dm:
        if "S" in x: continue
        C=x.get("C",[]); R=x.get("R",0); O=x.get("Ø",0); row=[]; ci=0
        for i in range(n):
            b=1<<i
            if R&b: row.append(prev[i])
            elif O&b: row.append(None)
            else: row.append(C[ci]); ci+=1
        prev=row[:]
        out=[]
        for i in range(n):
            v=row[i]
            if v is not None and DN[i] and isinstance(v,int) and DN[i] in dicts:
                d=dicts[DN[i]]; v=d[v] if 0<=v<len(d) else v
            out.append(v)
        rows.append(out)
    return N,T,DN,rows
for name,rk in [("weekly-peak-demand","405b6eb0-d87e-4828-b2dd-dcbae2ffa4b8"),("renewable-statistics","bb1027ef-65a1-47a0-b874-2f65cb80eeda")]:
    data=run(rk); N,T,DN,rows=decode(data["dsr"]["DS"][0])
    print(f"\n==== {name} ==== cols:",list(zip(N,T,DN)))
    print("nrows",len(rows))
    for r in rows[:8]:
        rr=[ (datetime.datetime.utcfromtimestamp(v/1000).strftime('%Y-%m-%d') if (T[i]==7 and isinstance(v,(int,float))) else v) for i,v in enumerate(r)]
        print("  ",rr)
