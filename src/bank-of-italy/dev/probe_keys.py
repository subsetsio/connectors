import time, json, nodes.bank_of_italy as m
from collections import Counter

# one std table + one measure table
for eid in ["AGGM0100", "PRINC_IND_01_01"]:
    m._seed_session()
    mem = m._member_series(eid, m.ENTITIES[eid])
    obs = m._fetch_group(mem[:3])
    rows = [o["values"] for o in obs if o.get("values")]
    keys = Counter()
    for r in rows:
        for k in r:
            keys[k] += 1
    n = len(rows)
    print(f"\n=== {eid}: members={len(mem)} sample_obs={n} ===")
    print("keys (count/total):", {k: f"{c}/{n}" for k, c in keys.items()})
    if rows:
        print("sample row:", json.dumps(rows[0], ensure_ascii=False))
