import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from utils import _odata_function, _fetch_json, OLINDA
from nodes.banco_central_do_brasil import _discover_sgs_series, _sgs_observations

def keys(rows, label):
    print(f"=== {label}: {len(rows)} rows ===")
    if rows:
        print(json.dumps(rows[0], ensure_ascii=False)[:600])

# IfDataValores one report
lista = _fetch_json(f"{OLINDA}/IFDATA/versao/v1/odata/ListaDeRelatorio()", {"$format":"json"}).get("value",[])
print("relatorios sample:", [r.get("NumeroRelatorio") for r in lista[:8]])
rel = str(lista[0]["NumeroRelatorio"])
rows = _odata_function("IFDATA","IfDataValores",{"AnoMes":202403,"TipoInstituicao":1,"Relatorio":f"'{rel}'"})
keys(rows, f"IfDataValores rel={rel}")

# SGS series catalog (just count + first)
series = _discover_sgs_series()
print(f"=== sgs series discovered: {len(series)} ===")
print(json.dumps(series[0], ensure_ascii=False) if series else "none")
# one series observations
if series:
    obs = _sgs_observations(series[0]["code"])
    print(f"sgs obs for code {series[0]['code']}: {len(obs)}")
    print(json.dumps(obs[0], ensure_ascii=False) if obs else "none")
