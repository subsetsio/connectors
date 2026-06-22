import io
import pandas as pd
from subsets_utils import get
BASE="https://www.dallasfed.org"
def raw(p):
    r=get(BASE+p,timeout=(10,120)); r.raise_for_status(); return r

# PCE text endpoints
for p in ["/~/media/documents/research/pce/pcedata","/~/media/documents/research/pce/pcehist","/~/media/documents/research/pce/tmrates.txt"]:
    print("\n##### PCE", p, "#####")
    try:
        r=raw(p); txt=r.content[:600].decode('latin-1',errors='replace')
        print("ct=",r.headers.get('content-type'),"len=",len(r.content))
        print(repr(txt[:600]))
    except Exception as e: print("ERR",type(e).__name__,e)

# WEI full history sheet
print("\n##### WEI 2008-current #####")
bio=io.BytesIO(raw("/-/media/documents/research/wei/weekly-economic-index.xlsx").content)
df=pd.read_excel(bio,sheet_name="2008-current",header=None,nrows=5)
with pd.option_context('display.max_columns',12,'display.width',200): print(df.to_string())

# agsurvey header detection across files
print("\n##### AGSURVEY header rows #####")
for f in ["agcredit","aglending","agrates","agrents","agvolume"]:
    bio=io.BytesIO(raw(f"/-/media/Documents/research/surveys/AgSurvey/data/{f}.xlsx").content)
    xl=pd.ExcelFile(bio)
    print(f"\n-- {f} sheets={xl.sheet_names}")
    sh=xl.sheet_names[0]
    df=xl.parse(sh,header=None,nrows=12)
    # find Date row
    for i in range(len(df)):
        c0=str(df.iloc[i,0])
        if c0.strip().lower()=="date":
            print(f"   Date header at row {i}; row-1:",list(df.iloc[i-1,:8].values) if i>0 else None)
            print(f"   header:",list(df.iloc[i,:8].values))
            print(f"   data row:",list(df.iloc[i+1,:8].values))
            break
    else:
        print("   no 'Date' in first col; col0 head:",list(df.iloc[:8,0].values))
