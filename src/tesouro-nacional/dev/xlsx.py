import io, pandas as pd
from subsets_utils import get
CKAN="https://www.tesourotransparente.gov.br/ckan/api/3/action"
def first(slug, fmt):
    r=get(f"{CKAN}/package_show",params={"id":slug},timeout=(10,120)); r.raise_for_status()
    for x in r.json()["result"]["resources"]:
        if (x.get("format") or "").upper()==fmt: return x["url"], x.get("name")
for slug,fmt in [("capag-municipios","XLSX"),("ds013","XLS"),("despesas-da-uniao-mensais-desde-2008","XLSX")]:
    u,nm=first(slug,fmt)
    b=get(u,timeout=(10,180)).content
    eng = "openpyxl" if fmt=="XLSX" else "xlrd"
    try:
        df=pd.read_excel(io.BytesIO(b), dtype=str, sheet_name=0, engine=eng)
        print(f"{slug} [{fmt}] {nm!r}: shape={df.shape} cols={list(df.columns)[:8]}")
    except Exception as e:
        print(f"{slug} [{fmt}] ERR {type(e).__name__}: {e}")
