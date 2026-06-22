import json
import nodes.bank_of_italy as m

eid = "TRI30101"
m._seed_session()
mem = m._member_series(eid, m.ENTITIES[eid])
print(f"{eid}: members={len(mem)}")

healthy_done = stripped_done = False
for node in mem:
    if healthy_done and stripped_done:
        break
    loc = node["localId"]
    try:
        report = m._service("GETDEFAULTREPORT", {"nodes": json.dumps([node])})
        prospetto = m._service("PROSPETTODATI", {
            "VIEW_MODE": "", "GRAPH_MODE": "lines", "COMM": "BANKITALIA", "CTX": "DIFF",
            "CUBEIDS": loc, "TABLEREQUEST": json.dumps(report),
        })
    except Exception as e:
        print(f"  loc={loc}: transient {type(e).__name__}; skip")
        continue
    obs = prospetto.get("GRAPHDATA", {}).get("observations", []) or []
    vals = [o.get("values") for o in obs if o.get("values")]
    if not vals:
        print(f"  loc={loc}: empty"); continue
    has_cubeid = "CUBEID" in vals[0]
    if has_cubeid and not healthy_done:
        cid = vals[0]["CUBEID"]
        print(f"  HEALTHY loc={loc}\n          CUBEID={cid}\n          match={cid==loc}")
        healthy_done = True
    elif not has_cubeid and not stripped_done:
        print(f"  STRIPPED loc={loc}  n={len(vals)}  keys={list(vals[0].keys())}")
        print("    sample:", json.dumps(vals[0], ensure_ascii=False))
        stripped_done = True
