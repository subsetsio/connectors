import io
import pyarrow.csv as pacsv
from subsets_utils import get

for fn in ["qog_bas_cs_jan26.csv", "qog_eqi_long_24.csv", "qog_eureg_wide2_nov20.csv"]:
    r = get("https://www.qogdata.pol.gu.se/data/" + fn, timeout=(10,300))
    r.raise_for_status()
    t = pacsv.read_csv(io.BytesIO(r.content))
    print(fn, "rows", t.num_rows, "cols", t.num_columns)
    print("  sample types:", [(f.name, str(f.type)) for f in t.schema][:6])
