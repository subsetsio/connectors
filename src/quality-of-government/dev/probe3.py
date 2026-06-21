import io
import pyarrow.csv as pacsv
from subsets_utils import get
for fn in ["qog_std_ts_jan26.csv", "qog_eqi_ind_24.csv"]:
    r = get("https://www.qogdata.pol.gu.se/data/" + fn, timeout=(10,300))
    r.raise_for_status()
    try:
        t = pacsv.read_csv(io.BytesIO(r.content))
        print(fn, "OK rows", t.num_rows, "cols", t.num_columns)
    except Exception as e:
        print(fn, "ERROR", type(e).__name__, str(e)[:200])
