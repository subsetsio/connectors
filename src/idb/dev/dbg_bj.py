import sys, io
sys.path.insert(0,'src')
from subsets_utils import get
url="https://data.iadb.org/file/download/b58cb948-edd5-4004-bb63-d190b74e931e"
r=get(url, timeout=120)
print("status:", r.status_code, "ctype:", r.headers.get("content-type"), "len:", len(r.content))
print("first bytes:", r.content[:16])
import pandas as pd
for eng in (None,"xlrd","openpyxl"):
    try:
        df=pd.read_excel(io.BytesIO(r.content), sheet_name=0, dtype=str, engine=eng)
        print(f"engine={eng}: shape={df.shape} cols={list(df.columns)[:6]}")
    except Exception as e:
        print(f"engine={eng}: ERR {type(e).__name__}: {str(e)[:120]}")
# list sheets
try:
    xl=pd.ExcelFile(io.BytesIO(r.content))
    print("sheets:", xl.sheet_names)
except Exception as e:
    print("ExcelFile ERR:", type(e).__name__, str(e)[:120])
