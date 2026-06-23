import json
from subsets_utils import get, post
HOST="https://wabi-south-africa-north-a-primary-api.analysis.windows.net"
RKS={"renewable-statistics":"bb1027ef-65a1-47a0-b874-2f65cb80eeda",
     "weekly-uclf-oclf-frequency":"55f5fb46-327d-4519-a113-dbda0646adc9",
     "financial-year-load-factor-eskom-ocgt":"b483c1a7-7cdc-4db7-8c70-117bb5836ac1",
     "weekly-peak-demand":"405b6eb0-d87e-4828-b2dd-dcbae2ffa4b8"}
def query(rk,pq):
    n=len(pq["Select"])
    me=get(f"{HOST}/public/reports/{rk}/modelsAndExploration?preferReadOnlySession=true",headers={"X-PowerBI-ResourceKey":rk},timeout=(10,60)).json()
    return me
for name,rk in RKS.items():
    H={"X-PowerBI-ResourceKey":rk}
    me=get(f"{HOST}/public/reports/{rk}/modelsAndExploration?preferReadOnlySession=true",headers=H,timeout=(10,60)).json()
    model=me["models"][0]; expl=me["exploration"]; reportId=expl.get("reportId")
    secs=expl["sections"]
    print(f"\n===== {name} :: sections={len(secs)} =====")
    vlist=[]
    for sec in secs:
        for vc in sec.get("visualContainers",[]):
            cfg=json.loads(vc.get("config","{}")); sv=cfg.get("singleVisual",{}); pq=sv.get("prototypeQuery")
            if pq: vlist.append((sv.get("visualType"),pq))
    print("visuals:",[(t,len(pq['Select'])) for t,pq in vlist])
    # query the largest with groups+measures
    cand=[(t,pq) for t,pq in vlist if any('Aggregation' in s for s in pq['Select']) and any('Aggregation' not in s for s in pq['Select'])]
    if not cand:
        print("NO group+measure visual; all:",[(t,[list(s)[0] for s in pq['Select']]) for t,pq in vlist][:2]); continue
    t,pq=max(cand,key=lambda x:len(x[1]['Select']))
    n=len(pq['Select'])
    body={"version":"1.0.0","queries":[{"Query":{"Commands":[{"SemanticQueryDataShapeCommand":{"Query":pq,
      "Binding":{"Primary":{"Groupings":[{"Projections":list(range(n))}]},"DataReduction":{"DataVolume":4,"Primary":{"Window":{"Count":50000}}},"Version":1}}}]},
      "QueryId":"","ApplicationContext":{"DatasetId":model["dbName"],"Sources":[{"ReportId":reportId}]}}],"cancelQueries":[],"modelId":model["id"]}
    r=post(f"{HOST}/public/reports/querydata?synchronous=true",headers={**H,"Content-Type":"application/json"},json=body,timeout=(10,120))
    print("visual",t,"status",r.status_code)
    if r.status_code!=200: print(r.text[:300]); continue
    data=r.json()["results"][0]["result"]["data"]
    names=[s.get("Name") for s in data["descriptor"]["Select"]]
    ds=data["dsr"]["DS"][0]
    print("DS keys",list(ds.keys()),"ValueDicts:",list(ds.get("ValueDicts",{}).keys()))
    dm=ds["PH"][0]["DM0"]
    Srow=next((x["S"] for x in dm if "S" in x),None)
    print("S types:",[(s["N"],s.get("T")) for s in Srow])
    print("names:",names)
    # show first data row raw
    draws=[x for x in dm if "S" not in x]
    print("first raw:",json.dumps(draws[0])[:300])
