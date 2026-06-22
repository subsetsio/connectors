import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import json
from utils import _odata_all, _odata_function, _fetch_json, OLINDA

def keys(rows, label):
    print(f"=== {label}: {len(rows)} rows ===")
    if rows:
        print(json.dumps(rows[0], ensure_ascii=False, indent=1)[:1200])

# Expectativas - one mensais set (small page)
url = f"{OLINDA}/Expectativas/versao/v1/odata/ExpectativaMercadoMensais"
r = _fetch_json(url, {"$format":"json","$top":3})
keys(r.get("value",[]), "ExpectativaMercadoMensais")

# Expectativas top5
url = f"{OLINDA}/Expectativas/versao/v1/odata/ExpectativasMercadoTop5Anuais"
r = _fetch_json(url, {"$format":"json","$top":3})
keys(r.get("value",[]), "ExpectativasMercadoTop5Anuais")

# PTAX dolar periodo (1 year)
rows = _odata_function("PTAX","CotacaoDolarPeriodo",
   {"dataInicial":"'01-01-2024'","dataFinalCotacao":"'01-31-2024'"})
keys(rows, "CotacaoDolarPeriodo")

# IFDATA cadastro one quarter
rows = _odata_function("IFDATA","IfDataCadastro",{"AnoMes":202403})
keys(rows, "IfDataCadastro 202403")
