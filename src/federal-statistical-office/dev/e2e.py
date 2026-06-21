import json, sys, os
sys.path.insert(0,"src")
# dev mode: CI unset -> writes to data/dev
from nodes.federal_statistical_office import fetch_one, DOWNLOAD_SPECS
from subsets_utils import load_raw_ndjson, duckdb
# pick a small multi-chunk cube
sid="federal-statistical-office-px-x-1304070000-101"
fetch_one(sid)
rows=load_raw_ndjson(sid)
print("rows:",len(rows),"cols:",list(rows[0].keys()))
# run the transform SQL against the raw via duckdb view
import subsets_utils.sql_transform as st
# emulate: register view then run sql
con=duckdb
# find raw file path
from subsets_utils.io import raw_uri
print("raw uri:", raw_uri(sid,"ndjson.gz"))
sql=f'SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value FROM read_json_auto("{raw_uri(sid,"ndjson.gz")}")'
res=duckdb.sql(sql)
print(res.limit(3))
print("transform row count:", duckdb.sql(f'SELECT count(*) FROM ({sql})').fetchone()[0])
