import os, json
os.environ.pop("CI", None)
os.environ["SUBSETS_DATA_DIR"] = os.path.abspath("dev/reprodata")
import nodes.bank_of_italy as m
from subsets_utils.io import save_raw_ndjson, raw_uri

eid = "TRI30021"
sid = "bank-of-italy-tri30021"
m._seed_session()
mem = m._member_series(eid, m.ENTITIES[eid])
groups = [mem[i:i+m.CHUNK_SIZE] for i in range(0, len(mem), m.CHUNK_SIZE)]
from concurrent.futures import ThreadPoolExecutor
rows = []
with ThreadPoolExecutor(max_workers=min(m._MAX_WORKERS, len(groups))) as p:
    for obs in p.map(m._fetch_group, groups):
        rows += [o["values"] for o in obs if o.get("values")]
print("total obs:", len(rows))
# Count CUBEID presence across ALL rows
missing = sum(1 for r in rows if "CUBEID" not in r)
print("rows missing CUBEID:", missing)
# how many of first 20480 have CUBEID
first = rows[:20480]
print("first-20480 missing CUBEID:", sum(1 for r in first if "CUBEID" not in r))
uri = save_raw_ndjson(rows, sid)
print("saved:", uri)

import duckdb
con = duckdb.connect()
# mimic reader: read_json_auto on the saved file
path = raw_uri(sid, "ndjson.zst")
print("reading", path)
schema = con.execute(f"DESCRIBE SELECT * FROM read_json_auto('{path}')").fetchall()
cols = [r[0] for r in schema]
print("inferred columns:", cols)
print("CUBEID present in inferred schema:", "CUBEID" in cols)
