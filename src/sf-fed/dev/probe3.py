import sys
sys.path.insert(0, "src")
from nodes.sf_fed import FILE_URL, _download, _melt_workbook
import pyarrow as pa
from nodes.sf_fed import SCHEMA

for slug, url in FILE_URL.items():
    try:
        content = _download(url)
        cols = _melt_workbook(content)
        tbl = pa.table(cols, schema=SCHEMA)
        sheets = sorted(set(cols["sheet"]))
        ndates = sum(1 for d in cols["period_date"] if d is not None)
        nval = sum(1 for v in cols["value"] if v is not None)
        ntext = sum(1 for v in cols["value_text"] if v is not None)
        print(f"{slug:55s} rows={len(tbl):7d} sheets={len(sheets)} dates={ndates:6d} num={nval:7d} txt={ntext:6d}")
        if len(tbl) == 0:
            print("   !!! ZERO ROWS, sheets seen:", sheets)
    except Exception as e:
        print(f"{slug:55s} ERROR {type(e).__name__}: {e}")
