import json, gzip, tempfile, os
import duckdb
from subsets_utils import get
import importlib.util

spec = importlib.util.spec_from_file_location("cobs", os.path.join(os.path.dirname(__file__), "..", "src", "nodes", "cobs.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# comets sample
cl = get(m.COMET_LIST_URL, params={"format": "json"}, timeout=(10, 120)).json()["objects"][:50]
# observations sample for id=1
obs = get(m.OBS_LIST_URL, params={"format": "json", "id": 1, "page": 1}, timeout=(10, 120)).json()["objects"]
flat = [m._flatten_observation(r, 1) for r in obs]

d = tempfile.mkdtemp()
cpath = os.path.join(d, "comets.ndjson.gz")
opath = os.path.join(d, "obs.ndjson.gz")
with gzip.open(cpath, "wt") as f:
    for r in cl: f.write(json.dumps(r) + "\n")
with gzip.open(opath, "wt") as f:
    for r in flat: f.write(json.dumps(r) + "\n")

con = duckdb.connect()
con.execute(f'CREATE VIEW "cobs-comets" AS SELECT * FROM read_json_auto(\'{cpath}\')')
con.execute(f'CREATE VIEW "cobs-observations" AS SELECT * FROM read_json_auto(\'{opath}\')')

csql = m.TRANSFORM_SPECS[0].sql
osql = m.TRANSFORM_SPECS[1].sql
cr = con.execute(csql).fetchall()
print("comets transform rows:", len(cr))
print("comets cols:", [d[0] for d in con.execute(csql).description])
orr = con.execute(osql).fetchall()
print("obs transform rows:", len(orr))
print("obs cols:", [d[0] for d in con.execute(osql).description])
print("sample obs row:", orr[0])
