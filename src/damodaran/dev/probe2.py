import sys, os, io
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import pandas as pd
from subsets_utils import get
def clean(v):
    if v is None: return ""
    s=str(v).strip(); return "" if s.lower()=="nan" else s
specials = {
 "histretsp":"histretSP","histimpl":"histimpl","ctryprem":"ctryprem",
 "countrytaxrates":"countrytaxrates","mktcaprisk":"mktcaprisk","macro":"macro",
 "mktcapmult":"mktcapmult","countrystats":"countrystats",
}
for fam,f in specials.items():
    r=get(f"https://pages.stern.nyu.edu/~adamodar/pc/datasets/{f}.xls",timeout=(10,120))
    if r.status_code!=200: print(fam,"HTTP",r.status_code); continue
    xls=pd.ExcelFile(io.BytesIO(r.content))
    print(f"\n#### {fam} ({f}.xls) sheets={xls.sheet_names}")
    for sh in xls.sheet_names:
        df=pd.read_excel(xls,sheet_name=sh,header=None,nrows=6)
        # show first cell of first 6 rows to locate header
        firsts=[clean(df.iloc[i,0]) for i in range(min(6,len(df)))]
        print(f"   [{sh}] {df.shape[1]}cols firstcol6={firsts}")
