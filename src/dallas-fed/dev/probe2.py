import io, sys
import pandas as pd
from subsets_utils import get
BASE="https://www.dallasfed.org"
def dl(p):
    r=get(BASE+p,timeout=(10,120)); r.raise_for_status(); return io.BytesIO(r.content), len(r.content)

# agvalue district full
print("##### AGVALUE district rows 6-20 #####")
bio,_=dl("/-/media/Documents/research/surveys/AgSurvey/data/agvalue.xlsx")
df=pd.read_excel(bio,sheet_name="district",header=None,skiprows=6,nrows=14)
with pd.option_context('display.max_columns',20,'display.width',220): print(df.to_string())

print("\n##### WEI #####")
bio,_=dl("/-/media/documents/research/wei/weekly-economic-index.xlsx")
xl=pd.ExcelFile(bio); print("sheets:",xl.sheet_names)
for sh in xl.sheet_names[:2]:
    print(f"-- {sh} --")
    with pd.option_context('display.max_columns',12,'display.width',200):
        print(xl.parse(sh,header=None,nrows=5).to_string())

print("\n##### HOUSEPRICE #####")
bio,_=dl("/-/media/Documents/research/international/houseprice/hp2504.xlsx")
xl=pd.ExcelFile(bio); print("sheets:",xl.sheet_names)
for sh in xl.sheet_names[:4]:
    print(f"-- {sh} --")
    with pd.option_context('display.max_columns',12,'display.width',200):
        print(xl.parse(sh,header=None,nrows=6).to_string())
