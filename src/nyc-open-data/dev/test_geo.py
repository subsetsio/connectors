import sys, os
sys.path.insert(0,"src"); os.environ.pop("CI",None)
from nodes.nyc_open_data import fetch_one
from subsets_utils import load_raw_parquet
sid="nyc-open-data-2i8t-es4u"  # VZV Arterial Slow Zones (MultiLine geometry)
fetch_one(sid)
t=load_raw_parquet(sid)
print("rows",t.num_rows,"cols",t.num_columns, [f.name for f in t.schema])
