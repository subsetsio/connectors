import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import io, pandas as pd
pd.set_option('display.max_columns',12); pd.set_option('display.width',220); pd.set_option('display.max_colwidth',26)

URLS={
 "gi-value":"https://www.fca.org.uk/publication/data/gi-value-measures-data-2024.xlsx",
 "psd-retail-inv":"https://www.fca.org.uk/publication/data/product-sales-data-retail-investments-2024.xlsx",
 "retail-interm":"https://www.fca.org.uk/publication/data/retail-intermediary-market-2024-underlying-data.xlsx",
 "retirement":"https://www.fca.org.uk/publication/data/retirement-income-underlying-data-2024-25.xlsx",
}
for k,u in URLS.items():
    print("#"*100); print(k)
    b=get(u, timeout=120).content
    xl=pd.ExcelFile(io.BytesIO(b))
    print("SHEETS:", xl.sheet_names)
    for sh in xl.sheet_names:
        df=xl.parse(sh, header=None, nrows=8)
        # count non-null cols
        print(f"--- {sh!r} ncols={df.shape[1]}")
        print(df.head(8).to_string())
