import gzip, sys
sys.path.insert(0, "src/nodes")
import importlib.util
spec = importlib.util.spec_from_file_location("dp", "src/nodes/debian_popcon.py")
dp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dp)
from subsets_utils import get
for nid, path in dp.VIEW_PATHS.items():
    content = get(dp.BASE_URL + path, timeout=(10.0,120.0)).content
    text = gzip.decompress(content).decode("utf-8","replace")
    rows = dp._parse(text)
    import pyarrow as pa
    tbl = pa.Table.from_pylist(rows, schema=dp.SCHEMA)
    names = set(r["name"] for r in rows)
    nmaint = sum(1 for r in rows if r["maintainer"])
    print(nid, "rows=", len(rows), "unique_names=", len(names), "with_maint=", nmaint)
    print("  first:", rows[0])
    print("  last :", rows[-1])
