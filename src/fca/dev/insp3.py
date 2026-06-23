import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import io, pandas as pd
pd.set_option('display.max_columns',30); pd.set_option('display.width',300); pd.set_option('display.max_colwidth',22)

# MLAR detailed file structure
u="https://www.fca.org.uk/publication/data/mlar-statistics-detailed-long-run.xlsx"
b=get(u, timeout=120).content
xl=pd.ExcelFile(io.BytesIO(b))
print("DETAILED SHEETS:", xl.sheet_names)
# look at one data sheet
for sh in xl.sheet_names:
    if sh.lower() in ("contents","detailed contents","notes"): 
        continue
    df=xl.parse(sh, header=None)
    print("="*90); print(f"SHEET {sh!r} shape={df.shape}")
    print(df.iloc[0:18, 0:14].to_string())
    break

# MLAR summary 1 data region
u2="https://www.fca.org.uk/publication/data/mlar-statistics-summary-long-run.xlsx"
b2=get(u2, timeout=120).content
df=pd.read_excel(io.BytesIO(b2), sheet_name="Summary 1", header=None)
print("@"*90); print("SUMMARY 1 shape", df.shape)
print(df.iloc[8:34, 0:14].to_string())
