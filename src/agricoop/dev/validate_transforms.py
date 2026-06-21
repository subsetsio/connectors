import sys, os, time, json, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import duckdb
from nodes.agricoop import _T, RESOURCE_ID, _PREFIX  # import the SQL + mapping
KEY=os.environ.get("DATA_GOV_IN_API_KEY","579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b")
BASE="https://api.data.gov.in/resource/"
def fetch_sample(rid, n=10):
    for a in range(12):
        r=get(BASE+rid, params={"api-key":KEY,"format":"json","offset":0,"limit":n}, timeout=(10,120))
        if r.status_code==429:
            time.sleep(20); continue
        return r.json().get("records") or []
    return []
for eid, rid in RESOURCE_ID.items():
    dep = _PREFIX + eid
    sql = _T[dep].format(dep=dep)
    rows = fetch_sample(rid)
    if not rows:
        print(f"!! {dep[:50]}: no sample rows (throttled?)"); continue
    # write tiny ndjson, register as view named dep, run sql
    tf = tempfile.NamedTemporaryFile("w", suffix=".ndjson", delete=False)
    for row in rows: tf.write(json.dumps(row)+"\n")
    tf.close()
    con = duckdb.connect()
    con.execute(f"CREATE VIEW \"{dep}\" AS SELECT * FROM read_json_auto('{tf.name}')")
    try:
        out = con.execute(sql).fetch_arrow_table()
        print(f"OK {dep[:55]:55s} -> {out.num_rows} rows, cols={out.column_names}")
    except Exception as e:
        print(f"FAIL {dep[:50]}: {type(e).__name__}: {e}")
    con.close(); os.unlink(tf.name)
    time.sleep(8)
