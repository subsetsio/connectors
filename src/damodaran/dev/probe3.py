import sys, os, io
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import pandas as pd
from subsets_utils import get
def clean(v):
    if v is None: return ""
    s=str(v).strip(); return "" if s.lower()=="nan" else s
# ctryprem ERPs by country: find the header row
r=get("https://pages.stern.nyu.edu/~adamodar/pc/datasets/ctryprem.xls",timeout=(10,120))
df=pd.read_excel(io.BytesIO(r.content),sheet_name="ERPs by country",header=None)
print("=== ctryprem 'ERPs by country' first col, rows 0-12 ===")
for i in range(min(13,len(df))):
    print(i, [clean(x)[:20] for x in df.iloc[i].tolist()[:8]])
print()
# DollarUS sheets + Industry Averages header
r2=get("https://pages.stern.nyu.edu/~adamodar/pc/datasets/DollarUS.xls",timeout=(10,120))
xls=pd.ExcelFile(io.BytesIO(r2.content))
print("=== DollarUS sheets:", xls.sheet_names)
for sh in xls.sheet_names:
    df2=pd.read_excel(xls,sheet_name=sh,header=None,nrows=12)
    print(f"--- [{sh}] ---")
    for i in range(min(12,len(df2))):
        print(i, [clean(x)[:18] for x in df2.iloc[i].tolist()[:8]])
