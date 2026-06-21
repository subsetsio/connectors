import io
import zipfile
import duckdb
import pyarrow.csv as pacsv
from subsets_utils import get
import sys
sys.path.insert(0, "src/nodes")
from cmhc import _transform_sql

for pid in ["34100140", "34100145", "34100133"]:
    url = f"https://www150.statcan.gc.ca/n1/tbl/csv/{pid}-eng.zip"
    r = get(url, timeout=(10.0, 120.0)); r.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(r.content))
    tbl = pacsv.read_csv(io.BytesIO(z.read(f"{pid}.csv")))
    asset = f"cmhc-{pid}"
    con = duckdb.connect()
    con.register(asset, tbl)
    sql = _transform_sql(asset)
    res = con.execute(sql).arrow()
    print("===", pid, "out rows:", res.num_rows, "cols:", res.column_names)
    print("   first row:", res.to_pylist()[0])
