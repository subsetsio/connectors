import ssl, json, io, zipfile
from subsets_utils import get

BASE = "https://datos.estadisticas.pr/api/3/action"

def show(pkg):
    r = get(f"{BASE}/package_show", params={"id": pkg}, timeout=(10,120))
    res = r.json()["result"]["resources"]
    print(f"\n=== {pkg} : {len(res)} resources ===")
    for x in res[:12]:
        print(f"  fmt={x.get('format'):6} name={(x.get('name') or '')[:40]:40} url=...{x.get('url','')[-40:]}")

for p in ["comercio-externo","nacimientos","encuesta-sobre-la-comunidad-de-puerto-rico-prcs",
          "mortalidad-infantil-cohortes","datos-del-tablero-indice-agricolas-resumen-censos-agricolas-2018-y-2022-por-regiones",
          "hipotecas-home-mortgage-disclosure-act-hmda"]:
    show(p)
