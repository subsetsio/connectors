"""Exercise fetch_one + the transform SQL locally on small domains (dev mode)."""
import os
os.environ.pop("CI", None)  # dev mode -> writes under data/dev

import pyarrow.parquet as pq
import duckdb
from subsets_utils import raw_parquet_localpath
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)) + "/src")
from nodes.fao import fetch_one, DOWNLOAD_SPECS, TRANSFORM_SPECS

# pick a couple of structurally diverse small domains
TARGETS = ["fao-mddw", "fao-pe", "fao-ae"]

specs = {s.id: s for s in DOWNLOAD_SPECS}
tspecs = {t.deps[0]: t for t in TRANSFORM_SPECS}

for sid in TARGETS:
    print(f"\n===== {sid} =====")
    fetch_one(sid)
    with raw_parquet_localpath(sid) as path:
        pf = pq.ParquetFile(path)
        print("rows:", pf.metadata.num_rows, "cols:", pf.schema.names)
        con = duckdb.connect()
        con.execute(f'''CREATE VIEW "{sid}" AS SELECT * FROM read_parquet('{path}')''')
        sql = tspecs[sid].sql
        res = con.execute(sql).fetch_arrow_table()
        print("transform rows:", res.num_rows)
        print("transform schema:", res.schema)
        print(res.slice(0, 3).to_pylist()[:2])
