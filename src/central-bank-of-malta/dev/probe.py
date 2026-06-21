import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import sys, io
import pandas as pd
from subsets_utils import get

BASE="https://www.centralbankmalta.org"
# representative files across sections + extensions
FILES = {
 "gdp-current (xls)": "/site/Subscriber Categories/Real Economy Indicators/gdp_current_2000.xls",
 "inflation-hicp (xlsx?)": "/site/Subscriber Categories/Real Economy Indicators/inflation-hicp.xlsx",
 "gross-gov-debt (xls)": "/site/Subscriber Categories/Govt Finance/gross_gov_debt.xls",
 "bop-financial (xlsx)": "/site/Subscriber Categories/External/bop_financial_accounts.xlsx",
 "balsheetcbm (xlsx)": "/site/Subscriber Categories/Monetary, Banking and Financial Markets/balsheetcbm.xlsx",
}
def fetch(path):
    url = BASE + "/" + "/".join(p for p in path.split("/") if p!="")
    # build proper url preserving spaces
    from urllib.parse import quote
    url = BASE + quote(path)
    r = get(url, timeout=(10,120))
    r.raise_for_status()
    return r.content

for name, path in FILES.items():
    print("="*70)
    print(name, path)
    try:
        content = fetch(path)
        print("  bytes:", len(content), "head:", content[:8])
        ext = path.rsplit(".",1)[-1].lower()
        eng = "openpyxl" if ext=="xlsx" else "xlrd"
        try:
            xls = pd.ExcelFile(io.BytesIO(content), engine=eng)
        except Exception as e:
            # try the other engine
            eng2 = "xlrd" if eng=="openpyxl" else "openpyxl"
            print("  engine", eng, "failed:", e, "-> trying", eng2)
            xls = pd.ExcelFile(io.BytesIO(content), engine=eng2)
            eng=eng2
        print("  engine:", eng, " sheets:", xls.sheet_names)
        df = pd.read_excel(xls, sheet_name=xls.sheet_names[0], header=None, nrows=15)
        print("  shape(first15):", df.shape)
        with pd.option_context('display.max_columns',12,'display.width',200):
            print(df.iloc[:15,:10].to_string())
    except Exception as e:
        import traceback; traceback.print_exc()
