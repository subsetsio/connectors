import sys, os
sys.path.insert(0, "src")
os.environ.pop("CI", None)
from nodes.nyc_open_data import fetch_one
from subsets_utils import load_raw_parquet
sid = "nyc-open-data-tg4x-b46p"
fetch_one(sid)
t = load_raw_parquet(sid)
print("rows", t.num_rows, "cols", t.num_columns)
print("schema:", [(f.name, str(f.type)) for f in t.schema][:6])
