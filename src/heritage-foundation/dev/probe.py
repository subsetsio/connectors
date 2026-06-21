import io
import pandas as pd
from subsets_utils import get

AZURE = "https://indexdotnet.azurewebsites.net/index/excel/{y}/index{y}_data.xls"
STATIC = "https://static.heritage.org/index/data/{y}/{y}_indexofeconomicfreedom_data.xlsx"

def fetch(url):
    r = get(url, timeout=(10,120))
    return r

def inspect(year, url, engine):
    r = fetch(url)
    ct = r.headers.get("content-type","")
    if r.status_code != 200 or "html" in ct.lower():
        print(f"  {year}: skip status={r.status_code} ct={ct}")
        return
    try:
        raw = pd.read_excel(io.BytesIO(r.content), sheet_name=0, header=None, engine=engine)
    except Exception as e:
        print(f"  {year}: read err {type(e).__name__} {e}")
        return
    print(f"  {year} engine={engine} shape={raw.shape} sheet0")
    for i in range(min(3, len(raw))):
        print(f"    row{i}:", [str(x)[:13] for x in raw.iloc[i].tolist()[:22]])

print("=== AZURE older years (header row 0, .xls, formula overall) ===")
for y in (2009, 2013):
    inspect(y, AZURE.format(y=y), "xlrd")
print("=== STATIC recent (banner row, .xlsx) ===")
for y in (2024, 2026):
    inspect(y, STATIC.format(y=y), "openpyxl")
