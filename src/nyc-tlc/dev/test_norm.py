import sys, tempfile, os
sys.path.insert(0, "src")
sys.path.insert(0, "src/nodes")
import duckdb
from subsets_utils import get
import nyc_tlc as N

def norm_schema(url, colspecs):
    r = get(url, timeout=(10,300)); r.raise_for_status()
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=".parquet"); tf.write(r.content); tf.close()
    con = duckdb.connect()
    sql = N._projection_sql(con, tf.name, colspecs)
    reader = con.sql(sql).fetch_record_batch(200_000)
    sch = reader.schema
    nrows = 0
    for b in reader:
        nrows += b.num_rows
        if nrows >= 200_000: break  # just sample a couple batches
    con.close(); os.unlink(tf.name)
    return sch, nrows

for label, url, cs in [
    ("yellow 2009-01", f"{N.BASE}/yellow_tripdata_2009-01.parquet", N._YELLOW),
    ("yellow 2025-02", f"{N.BASE}/yellow_tripdata_2025-02.parquet", N._YELLOW),
    ("green 2014-01",  f"{N.BASE}/green_tripdata_2014-01.parquet",  N._GREEN),
    ("fhv 2015-01",    f"{N.BASE}/fhv_tripdata_2015-01.parquet",    N._FHV),
    ("fhvhv 2019-02",  f"{N.BASE}/fhvhv_tripdata_2019-02.parquet",  N._FHVHV),
]:
    sch, n = norm_schema(url, cs)
    fields = [(f.name, str(f.type)) for f in sch]
    print(f"### {label}  rows_sampled>={n}")
    print("   ", fields)
