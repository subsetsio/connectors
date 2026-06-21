import os, duckdb
os.environ.pop("CI", None)  # local dev -> data/dev/
import sys; sys.path.insert(0, "src")
from nodes.fcc import fetch_one
from subsets_utils import list_raw_files
from subsets_utils.config import raw_uri

sid = "fcc-xqgr-24et"  # Pirate Radio, 185 rows
fetch_one(sid)
files = list_raw_files(f"{sid}.*")
print("raw files:", files)
uri = raw_uri(sid, "csv.gz")
print("uri:", uri)
con = duckdb.connect()
n = con.execute(f"SELECT count(*) FROM read_csv_auto('{uri}')").fetchone()[0]
cols = con.execute(f"SELECT * FROM read_csv_auto('{uri}') LIMIT 1").description
print("rows:", n, "ncols:", len(cols))
print("cols:", [c[0] for c in cols])
