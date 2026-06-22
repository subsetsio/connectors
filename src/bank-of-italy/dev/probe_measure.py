import json
import nodes.bank_of_italy as m
from collections import Counter

eid = "PRINC_IND_01_01"
m._seed_session()
mem = m._member_series(eid, m.ENTITIES[eid])
print(f"members={len(mem)}; sample member localId={mem[0]['localId']}")

# Replicate _try_chunk WITHOUT the degraded-raise so we can see real keys.
chunk = mem[:3]
report = m._service("GETDEFAULTREPORT", {"nodes": json.dumps(chunk)})
prospetto = m._service("PROSPETTODATI", {
    "VIEW_MODE": "", "GRAPH_MODE": "lines", "COMM": "BANKITALIA", "CTX": "DIFF",
    "CUBEIDS": ";".join(n["localId"] for n in chunk),
    "TABLEREQUEST": json.dumps(report),
})
obs = prospetto.get("GRAPHDATA", {}).get("observations", []) or []
rows = [o.get("values") for o in obs if o.get("values")]
keys = Counter()
for r in rows:
    for k in r:
        keys[k] += 1
n = len(rows)
print(f"obs={n}")
print("keys:", {k: f"{c}/{n}" for k, c in keys.items()})
if rows:
    print("sample:", json.dumps(rows[0], ensure_ascii=False))
