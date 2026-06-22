import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import importlib.util
spec = importlib.util.spec_from_file_location("bbmod", os.path.join(os.path.dirname(__file__),"..","src","nodes","bundesbank.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
n = m._fetch_freq("__scratch_bbbk7_Q", "BBBK7", "Q")
print("Q rows written:", n)
import pyarrow.parquet as pq
from subsets_utils.io import raw_uri
uri = raw_uri("__scratch_bbbk7_Q","parquet")
t = pq.read_table(uri)
print("parquet rows:", t.num_rows, "cols:", t.column_names)
print("sample series_id:", t.column("series_id")[0].as_py())
print("sample dataflow:", t.column("dataflow")[0].as_py())
print("value type:", t.schema.field("value").type)
import re
# verify matches-pattern belief: series_id starts with 'BBBK7.'
sids = t.column("series_id").to_pylist()[:1000]
bad = [s for s in sids if not re.fullmatch(r"BBBK7\..*", s)]
print("series_id not matching BBBK7\\..* (first1000):", len(bad), bad[:3])
