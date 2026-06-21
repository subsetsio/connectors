import io, zipfile
import pandas as pd
from subsets_utils import get
BASE="https://datos.estadisticas.pr/api/3/action"
def resources(pkg):
    r=get(f"{BASE}/package_show",params={"id":pkg},timeout=(10,180)); r.raise_for_status()
    return r.json()["result"]["resources"]
for p in ["comercio-externo","mortalidad-infantil-cohortes",
          "datos-del-tablero-indice-agricolas-resumen-censos-agricolas-2018-y-2022-por-regiones",
          "hipotecas-home-mortgage-disclosure-act-hmda","commuting-flow-2009-2015"]:
    res=resources(p)
    fmts={}
    for x in res: fmts[(x.get('format') or '').upper()]=fmts.get((x.get('format') or '').upper(),0)+1
    print(f"\n=== {p}: {len(res)} res {fmts} ===")
    for x in res:
        fmt=(x.get('format') or '').upper()
        if fmt in ("PDF","KML",""): continue
        url=x.get('url')
        try:
            d=get(url,timeout=(10,180)); d.raise_for_status(); c=d.content
            if fmt in ("CSV","TXT"):
                df=pd.read_csv(io.BytesIO(c),dtype=str,nrows=3,sep=None,engine="python")
                print(f"  {fmt} {len(c)}B rows~ cols={len(df.columns)} {list(df.columns)[:6]}")
            elif fmt in ("XLSX","XLS"):
                xl=pd.ExcelFile(io.BytesIO(c)); print(f"  {fmt} {len(c)}B sheets={xl.sheet_names[:5]}")
                df=xl.parse(xl.sheet_names[0],dtype=str,nrows=3); print(f"     cols={list(df.columns)[:6]}")
            elif fmt=="ZIP":
                z=zipfile.ZipFile(io.BytesIO(c)); names=z.namelist()
                print(f"  ZIP {len(c)}B members({len(names)})={names[:6]}")
            elif fmt=="JSON":
                import json; j=json.loads(c); print(f"  JSON type={type(j).__name__} sample={str(j)[:100]}")
        except Exception as e:
            print(f"  {fmt} ERR {type(e).__name__}: {str(e)[:80]}")
        break
