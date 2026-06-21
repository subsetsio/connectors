"""Local end-to-end sanity check for ONE small dataflow (CCIR) via the parquet path.

Exercises the real raw_parquet_writer -> load_raw_parquet -> DuckDB transform
path the cloud run uses, without running the whole connector. Writes to the
local dev data dir (CI unset). Not a production path.
"""
import csv, io
import pyarrow as pa
import duckdb
from subsets_utils import get, raw_parquet_writer, load_raw_parquet
from subsets_utils.sql_transform import _read_clause

ASSET = "bank-of-israel-ccir"
URL = "https://edge.boi.org.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/CCIR/1.0?format=csv"

def to_batch(rows, schema):
    cols = list(zip(*rows)) if rows else [() for _ in schema]
    return pa.RecordBatch.from_arrays([pa.array(list(c), type=pa.string()) for c in cols], schema=schema)

text = get(URL, timeout=(10.0, 120.0)).text
reader = csv.reader(io.StringIO(text))
header = next(reader)
ncol = len(header)
schema = pa.schema([(c, pa.string()) for c in header])
n = 0
with raw_parquet_writer(ASSET, schema) as w:
    buf = []
    for row in reader:
        if len(row) < ncol: row = row + [""] * (ncol - len(row))
        elif len(row) > ncol: row = row[:ncol]
        buf.append(row)
    w.write_batch(to_batch(buf, schema)); n = len(buf)
print("wrote rows:", n)

tbl = load_raw_parquet(ASSET)
print("loaded rows:", tbl.num_rows, "| cols:", len(tbl.column_names))

rels, clause = _read_clause(ASSET)
print("read clause:", clause[:160])
duckdb.sql(f'CREATE OR REPLACE TEMP VIEW "{ASSET}" AS SELECT * FROM {clause}')
sql = f'''
    SELECT * REPLACE (CAST(OBS_VALUE AS DOUBLE) AS OBS_VALUE)
    FROM "{ASSET}"
    WHERE TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
'''
out = duckdb.sql(sql).fetch_arrow_table()
print("transform rows:", out.num_rows, "| OBS_VALUE type:", out.schema.field("OBS_VALUE").type)
print("sample:", out.slice(0, 1).to_pylist())
