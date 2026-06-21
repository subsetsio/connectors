import io, json, sys
import pandas as pd
from subsets_utils import get

files = json.load(open("dev/files.json"))
BASE = "https://www.policyuncertainty.com/media/"

# A diverse sample across file types/layouts.
sample = [
    "us-policy-uncertainty-data",
    "all-country-data",
    "all-daily-policy-data",
    "categorical-epu-data",
    "global-policy-uncertainty-data",
    "denmark-monthly",
    "uct",
    "cpu-base-pos-neg-all-countries-monthly",
    "energy-related-uncertainty-indexes",
    "hk-epu-data-annotated",
    "korea-categorical-pu-indices",
    "all-daily-aieu-data",
    "state-policy-uncertainty",
    "ecsu-index",
    "india-gui-index-data",
]
which = sys.argv[1:] or sample

for eid in which:
    fn = files[eid]
    url = BASE + fn.replace(" ", "%20")
    try:
        r = get(url, timeout=(10, 120))
        r.raise_for_status()
        content = r.content
    except Exception as e:
        print(f"\n==== {eid} ({fn}) FETCH ERROR: {e}")
        continue
    print(f"\n==== {eid}  |  {fn}  |  {len(content)} bytes")
    try:
        if fn.lower().endswith(".csv"):
            df = pd.read_csv(io.BytesIO(content))
            print("CSV sheet")
            print("cols:", list(df.columns))
            print(df.head(4).to_string())
            print("tail:")
            print(df.tail(3).to_string())
            print("dtypes:", dict(df.dtypes.astype(str)))
        else:
            eng = "xlrd" if fn.lower().endswith(".xls") else "openpyxl"
            xl = pd.ExcelFile(io.BytesIO(content), engine=eng)
            print("sheets:", xl.sheet_names)
            for sh in xl.sheet_names[:2]:
                df = xl.parse(sh, header=None, nrows=8)
                print(f"-- sheet {sh!r} raw head (no header):")
                print(df.to_string())
    except Exception as e:
        print(f"  PARSE ERROR: {type(e).__name__}: {e}")
