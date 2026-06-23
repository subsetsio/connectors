import io, pandas as pd
from subsets_utils import get
for url in ["https://www.frbsf.org/wp-content/uploads/twelfth-district-business-sentiment-data.xlsx"]:
    r=get(url,timeout=(10,90)); xl=pd.ExcelFile(io.BytesIO(r.content))
    print("TWELFTH sheets:", xl.sheet_names)
    for sh in xl.sheet_names:
        df=xl.parse(sh,header=None,nrows=6)
        print(f"--- {sh} ({df.shape[1]} cols)")
        for i,row in df.iterrows():
            print("   r%d:"%i," | ".join(str(v)[:20] for v in row.tolist()[:7]))
# tfp nodate periods
import sys; sys.path.insert(0,"dev"); from parser import parse_workbook
r=get("https://www.frbsf.org/wp-content/uploads/quarterly_tfp.xlsx",timeout=(10,90))
rows=parse_workbook(r.content,"quarterly_tfp")
nd=set(x['period'] for x in rows if not x['date'])
print("\nTFP nodate distinct periods (sample):", sorted(nd)[:20], " count=",len(nd))
