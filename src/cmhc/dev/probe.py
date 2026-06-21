import io
import zipfile
import pyarrow.csv as pacsv
from subsets_utils import get

# Probe two different StatCan tables to see column variability + types.
for pid in ["34100140", "34100145"]:
    url = f"https://www150.statcan.gc.ca/n1/tbl/csv/{pid}-eng.zip"
    r = get(url, timeout=(10.0, 120.0))
    r.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(r.content))
    print("===", pid, "names:", z.namelist())
    data_name = f"{pid}.csv"
    raw = z.read(data_name)
    tbl = pacsv.read_csv(io.BytesIO(raw))
    print("rows:", tbl.num_rows)
    for f in tbl.schema:
        print("   ", repr(f.name), f.type)
    # show a couple sample rows of REF_DATE / VALUE
    d = tbl.to_pylist()[:2]
    print("sample:", {k: d[0].get(k) for k in ("REF_DATE", "GEO", "VALUE", "UOM")})
