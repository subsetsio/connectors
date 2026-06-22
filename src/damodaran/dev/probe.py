import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import io, pandas as pd
from subsets_utils import get

def look(url, label):
    print("="*70); print(label, url)
    r = get(url, timeout=(10,120))
    print("status", r.status_code, "bytes", len(r.content), "ctype", r.headers.get("content-type"))
    if r.status_code != 200: return
    try:
        xls = pd.ExcelFile(io.BytesIO(r.content))  # xlrd for .xls
        print("sheets:", xls.sheet_names)
        for sh in xls.sheet_names[:2]:
            df = pd.read_excel(xls, sheet_name=sh, header=None, nrows=12)
            print(f"--- sheet '{sh}' first 12 rows x {df.shape[1]} cols ---")
            for i,row in df.iterrows():
                vals = [str(v)[:18] for v in row.tolist()[:10]]
                print(i, vals)
    except Exception as e:
        print("PARSE ERR", type(e).__name__, e)

look("https://pages.stern.nyu.edu/~adamodar/pc/datasets/betas.xls", "CURRENT betas")
look("https://pages.stern.nyu.edu/~adamodar/pc/datasets/margin.xls", "CURRENT margin")
look("https://pages.stern.nyu.edu/~adamodar/pc/archives/betas10.xls", "ARCHIVE betas10")
