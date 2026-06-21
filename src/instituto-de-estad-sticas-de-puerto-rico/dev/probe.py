import ssl, io, zipfile
import pandas as pd
from subsets_utils import get, configure_http

INTERMEDIATE_PEM = open("/tmp/rapidssl.pem").read()
ctx = ssl.create_default_context()
ctx.load_verify_locations(cadata=INTERMEDIATE_PEM)
configure_http(verify=ctx)

BASE = "https://datos.estadisticas.pr/api/3/action"

def resources(pkg):
    r = get(f"{BASE}/package_show", params={"id": pkg}, timeout=(10,120))
    r.raise_for_status()
    return r.json()["result"]["resources"]

for p in ["comercio-externo","nacimientos","mortalidad-infantil-cohortes",
          "datos-del-tablero-indice-agricolas-resumen-censos-agricolas-2018-y-2022-por-regiones",
          "hipotecas-home-mortgage-disclosure-act-hmda"]:
    res = resources(p)
    print(f"\n=== {p} : {len(res)} resources ===")
    for x in res[:8]:
        print(f"  fmt={(x.get('format') or '').upper():6} name={(x.get('name') or '')[:45]:45}")
    # try first non-pdf resource
    for x in res:
        fmt=(x.get('format') or '').upper()
        if fmt in ("PDF","KML",""): continue
        url=x.get('url')
        try:
            d=get(url, timeout=(10,120)); d.raise_for_status()
            content=d.content
            print(f"  -> fetched {fmt} {len(content)}B from {url[-45:]}")
            if fmt=="CSV" or fmt=="TXT":
                df=pd.read_csv(io.BytesIO(content), dtype=str, nrows=5, sep=None, engine="python")
                print(f"     cols({len(df.columns)}): {list(df.columns)[:10]}")
            elif fmt in ("XLSX","XLS"):
                df=pd.read_excel(io.BytesIO(content), dtype=str, nrows=5)
                print(f"     cols({len(df.columns)}): {list(df.columns)[:10]}")
            elif fmt=="ZIP":
                z=zipfile.ZipFile(io.BytesIO(content))
                print(f"     zip members: {z.namelist()[:10]}")
            elif fmt=="JSON":
                print(f"     json head: {content[:120]}")
        except Exception as e:
            print(f"  -> ERR {fmt} {type(e).__name__}: {e}")
        break
