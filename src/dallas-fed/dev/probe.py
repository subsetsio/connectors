import io, sys
import pandas as pd
from subsets_utils import get

BASE = "https://www.dallasfed.org"
def dl(path):
    r = get(BASE + path, timeout=(10,120))
    r.raise_for_status()
    return io.BytesIO(r.content), len(r.content)

def inspect(path, engine=None, n=6):
    print("\n" + "="*70)
    print("URL:", path)
    bio, ln = dl(path)
    print("bytes:", ln)
    try:
        xl = pd.ExcelFile(bio, engine=engine)
    except Exception as e:
        print("  ExcelFile err:", type(e).__name__, e)
        return
    print("sheets:", xl.sheet_names)
    for sh in xl.sheet_names[:3]:
        print(f"\n--- sheet '{sh}' (header=None, first {n} rows) ---")
        df = xl.parse(sh, header=None, nrows=n)
        with pd.option_context('display.max_columns', 14, 'display.width', 200):
            print(df.to_string())

targets = {
 "tmos_alldata":   "/~/media/Documents/research/surveys/tmos/documents/alldata.xls",
 "tmos_index":     "/~/media/Documents/research/surveys/tmos/documents/index.xls",
 "des_qq":         "/~/media/Documents/research/surveys/des/documents/all_data_qq.xlsx",
 "agvalue":        "/-/media/Documents/research/surveys/AgSurvey/data/agvalue.xlsx",
 "bcs_all":        "/~/media/Documents/research/surveys/bcs/documents/BCS_All_Results.xls",
 "wei":            "/-/media/documents/research/wei/weekly-economic-index.xlsx",
 "houseprice":     "/-/media/Documents/research/international/houseprice/hp2504.xlsx",
}
which = sys.argv[1] if len(sys.argv)>1 else "all"
for k,p in targets.items():
    if which!="all" and k!=which: continue
    try:
        inspect(p)
    except Exception as e:
        print("ERR", k, type(e).__name__, e)
