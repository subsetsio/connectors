import collections, nodes.bank_of_italy as m
eid = "TRI30021"
m._seed_session()
mem = m._member_series(eid, m.ENTITIES[eid])
groups = [mem[i:i+m.CHUNK_SIZE] for i in range(0, len(mem), m.CHUNK_SIZE)]
from concurrent.futures import ThreadPoolExecutor
rows = []
with ThreadPoolExecutor(max_workers=min(m._MAX_WORKERS, len(groups))) as p:
    for obs in p.map(m._fetch_group, groups):
        rows += [o["values"] for o in obs if o.get("values")]
print("obs:", len(rows))
keys = collections.Counter()
for r in rows[:2000]:
    keys.update(r.keys())
print("columns:", dict(keys))
if rows:
    print("sample:", rows[0])
