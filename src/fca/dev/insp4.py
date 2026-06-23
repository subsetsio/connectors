import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import io, pandas as pd
pd.set_option('display.max_columns',16); pd.set_option('display.width',260); pd.set_option('display.max_colwidth',30)

# retail-intermediary section 1 region
b=get("https://www.fca.org.uk/publication/data/retail-intermediary-market-2024-underlying-data.xlsx",timeout=120).content
df=pd.read_excel(io.BytesIO(b), sheet_name="Data tables - Section 1", header=None)
print("RETAIL-INTERM Section1 shape",df.shape)
print(df.iloc[5:30,0:12].to_string())

# gi Product Table - read whole
b2=get("https://www.fca.org.uk/publication/data/gi-value-measures-data-2024.xlsx",timeout=120).content
pt=pd.read_excel(io.BytesIO(b2), sheet_name="Product Table", header=None)
print("@"*80,"GI Product Table shape",pt.shape)
print(pt.iloc[0:12,0:12].to_string())
