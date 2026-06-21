import io
import pandas as pd
from subsets_utils import get
from nodes.eu_klems import _normalize_long, _to_arrow, _MODULE_FILE, _BULK_BASE

# Full-data check on the trickiest two: a wide-by-year module (Capital, biggest)
# and a long-by-year/wide-by-var module (Intangibles).
for eid in ["statistical-capital", "analytical-intangibles", "statistical-labour"]:
    content = get(_BULK_BASE + _MODULE_FILE[eid], timeout=(10.0, 180.0)).content
    df = pd.read_csv(io.BytesIO(content))
    long = _normalize_long(df)
    tbl = _to_arrow(long)
    print(f"=== {eid}")
    print(f"  wide shape {df.shape} -> long rows {len(long):,}")
    print(f"  arrow cols: {[f.name for f in tbl.schema]}")
    print(f"  arrow types: {[str(f.type) for f in tbl.schema]}")
    print(f"  distinct var: {long['var'].nunique()}  year range: {long['year'].min()}-{long['year'].max()}")
    print(f"  sample: {tbl.slice(0,1).to_pylist()[0]}")
