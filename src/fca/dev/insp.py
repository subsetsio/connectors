import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get
import io, pandas as pd

URLS={
 "mlar-summary":"https://www.fca.org.uk/publication/data/mlar-statistics-summary-long-run.xlsx",
 "complaints-agg":"https://www.fca.org.uk/publication/data/aggregate-complaints-data-2025-h2.xlsx",
 "complaints-firm":"https://www.fca.org.uk/publication/data/firm-level-complaints-data-2025-h2.xlsx",
}
for k,u in URLS.items():
    print("#"*90); print(k, u)
    b=get(u, timeout=120).content
    xl=pd.ExcelFile(io.BytesIO(b))
    print("SHEETS:", xl.sheet_names)
    for sh in xl.sheet_names[:6]:
        df=xl.parse(sh, header=None, nrows=12)
        print(f"--- sheet {sh!r}  full_shape rows~ (showing 12)  ncols={df.shape[1]}")
        with pd.option_context('display.max_columns',20,'display.width',200,'display.max_colwidth',28):
            print(df.head(12).to_string())
