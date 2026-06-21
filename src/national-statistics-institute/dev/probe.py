from subsets_utils import get
import json
def fetch(u):
    r = get(u, timeout=(10,120)); r.raise_for_status(); return r.json()
# full history (no nult) for a small table
d = fetch("https://servicios.ine.es/wstempus/js/EN/DATOS_TABLA/28481")
print("num series:", len(d))
s0 = d[0]
print("series0 keys:", list(s0.keys()))
print("series0 COD/Nombre/FK_Unidad/FK_Escala:", s0.get("COD"), "|", s0.get("Nombre"), "|", s0.get("FK_Unidad"), "|", s0.get("FK_Escala"))
print("series0 Data len:", len(s0["Data"]))
print("Data[0] keys:", list(s0["Data"][0].keys()))
print("Data[0]:", s0["Data"][0])
print("Data[-1]:", s0["Data"][-1])
# check value types / nulls / secret
vals = [dp.get("Valor") for se in d for dp in se["Data"]]
print("total points:", len(vals), "nulls:", sum(1 for v in vals if v is None), "sample vals:", vals[:5])
print("Valor types:", set(type(v).__name__ for v in vals))
secrets = [dp.get("Secreto") for se in d for dp in se["Data"]]
print("secret types:", set(type(s).__name__ for s in secrets), "any true:", any(secrets))
# Anyo type
print("Anyo type:", type(s0["Data"][0].get("Anyo")).__name__, "FK_Periodo:", s0["Data"][0].get("FK_Periodo"), "FK_TipoDato:", s0["Data"][0].get("FK_TipoDato"))
