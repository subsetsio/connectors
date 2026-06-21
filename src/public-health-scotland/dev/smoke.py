import sys
sys.path.insert(0,"src"); sys.path.insert(0,"src/nodes")
from nodes.public_health_scotland import fetch_one
from subsets_utils import load_raw_parquet
sid="public-health-scotland-urban-rural-classification"
fetch_one(sid)
t=load_raw_parquet(sid)
print("ROWS",len(t),"COLS",len(t.column_names))
print("colnames sample:", t.column_names[:12])
import pyarrow.compute as pc
print("resource_name nulls:", t.column("resource_name").null_count)
print("distinct resources:", pc.count_distinct(t.column("resource_name")).as_py())
