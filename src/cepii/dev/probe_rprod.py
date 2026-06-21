import io
import pandas as pd
from subsets_utils import get
r = get("https://www.cepii.fr/DATA_DOWNLOAD/EQCHANGE/RPROD.xls", timeout=(10, 120)); r.raise_for_status()
xl = pd.ExcelFile(io.BytesIO(r.content))
print("sheets:", xl.sheet_names)
for sh in xl.sheet_names[:6]:
    df = xl.parse(sh, header=None, nrows=8)
    print(f"\n== sheet {sh!r} shape(head)={df.shape}")
    print(df.to_string(max_cols=12))
