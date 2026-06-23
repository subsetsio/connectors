import json
from subsets_utils import get, post
HOST="https://wabi-south-africa-north-a-primary-api.analysis.windows.net"
def mae(rk):
    return get(f"{HOST}/public/reports/{rk}/modelsAndExploration?preferReadOnlySession=true",headers={"X-PowerBI-ResourceKey":rk},timeout=(10,60)).json()
def run(rk, pq, count=50000):
    me=mae(rk); model=me["models"][0]; expl=me["exploration"]
    n=len(pq["Select"])
    body={"version":"1.0.0","queries":[{"Query":{"Commands":[{"SemanticQueryDataShapeCommand":{"Query":pq,
      "Binding":{"Primary":{"Groupings":[{"Projections":list(range(n))}]},"DataReduction":{"DataVolume":4,"Primary":{"Window":{"Count":count}}},"Version":1}}}]},
      "QueryId":"","ApplicationContext":{"DatasetId":model["dbName"],"Sources":[{"ReportId":expl.get("reportId")}]}}],"cancelQueries":[],"modelId":model["id"]}
    r=post(f"{HOST}/public/reports/querydata?synchronous=true",headers={"X-PowerBI-ResourceKey":rk,"Content-Type":"application/json"},json=body,timeout=(10,120))
    return r.json()["results"][0]["result"]["data"]
def biggest_visual(rk):
    me=mae(rk)
    vs=[]
    for sec in me["exploration"]["sections"]:
        for vc in sec.get("visualContainers",[]):
            cfg=json.loads(vc.get("config","{}")); pq=cfg.get("singleVisual",{}).get("prototypeQuery")
            if pq and any('Aggregation' in s for s in pq['Select']) and any('Aggregation' not in s for s in pq['Select']):
                vs.append(pq)
    return max(vs,key=lambda p:len(p['Select']))

for name,rk in [("weekly-peak-demand","405b6eb0-d87e-4828-b2dd-dcbae2ffa4b8"),
                ("renewable-statistics","bb1027ef-65a1-47a0-b874-2f65cb80eeda")]:
    pq=biggest_visual(rk)
    data=run(rk,pq)
    ds=data["dsr"]["DS"][0]
    print(f"\n===== {name} =====")
    print("full S:", json.dumps(next(x['S'] for x in ds['PH'][0]['DM0'] if 'S' in x)))
    print("ValueDicts keys+lens:", {k:len(v) for k,v in ds.get("ValueDicts",{}).items()})
    for k,v in ds.get("ValueDicts",{}).items():
        print(f"  {k} sample:", v[:6])
    dm=ds["PH"][0]["DM0"]
    draws=[x for x in dm if "S" not in x]
    print("n rows", len(draws), "first 4 raw:")
    for r in draws[:4]: print("  ",json.dumps(r)[:200])
