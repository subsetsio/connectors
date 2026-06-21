import sys; sys.path.insert(0,"src")
import os
# CI unset -> writes to data/dev/
os.environ.pop("CI", None)
import duckdb
from nodes.environment_and_climate_change_canada import fetch_one, _collection_of
from subsets_utils import load_raw_ndjson

sid="environment-and-climate-change-canada-aqhi-stations"
fetch_one(sid)
rows=load_raw_ndjson(sid)
print("rows:",len(rows))
print("sample keys:", sorted(rows[0].keys()))
print("feature_id sample:", rows[0].get("feature_id"))
# emulate transform: register view over rows, run SELECT *
con=duckdb.connect()
import pyarrow as pa, json
# write rows to a temp ndjson for duckdb read
import tempfile, gzip
tf=tempfile.NamedTemporaryFile(suffix=".ndjson", delete=False, mode="w")
for r in rows: tf.write(json.dumps(r)+"\n")
tf.close()
con.execute(f"CREATE VIEW v AS SELECT * FROM read_json_auto('{tf.name}')")
res=con.execute('SELECT count(*) c, count(DISTINCT feature_id) d FROM v WHERE feature_id IS NOT NULL').fetchone()
print("transform rows / distinct feature_id:", res)
cols=[c[0] for c in con.execute("SELECT * FROM v LIMIT 0").description]
print("transform columns:", cols)
