import io
import pandas as pd
from subsets_utils import get
BASE="https://www.dallasfed.org"
def bio(p): 
    r=get(BASE+p,timeout=(10,120)); r.raise_for_status(); return io.BytesIO(r.content)

for name,p in [("tssos","/~/media/Documents/research/surveys/tssos/documents/tssos_alldata.xls"),
               ("tros","/-/media/Documents/research/surveys/tssos/documents/tros_alldata.xls")]:
    print(f"\n##### {name} #####")
    xl=pd.ExcelFile(bio(p)); print("sheets:",xl.sheet_names)
    df=xl.parse(xl.sheet_names[0],header=None,nrows=2)
    print("hdr:",list(df.iloc[0,:10].values)); print("row1:",list(df.iloc[1,:6].values))

for name,p in [("pcedata","/~/media/documents/research/pce/pcedata"),
               ("pcehist","/~/media/documents/research/pce/pcehist")]:
    print(f"\n##### {name} #####")
    xl=pd.ExcelFile(bio(p)); print("sheets:",xl.sheet_names)
    for sh in xl.sheet_names[:3]:
        df=xl.parse(sh,header=None,nrows=6)
        print(f"-- {sh} shape rows --")
        with pd.option_context('display.max_columns',12,'display.width',200): print(df.to_string())
