from subsets_utils import get
import httpx

base = "https://ws01.cenace.gob.mx:8082/SWPEND/SIM/SIN/MDA"
date = "2024/06/01/2024/06/01/JSON"
def vals(url):
    r = get(url, timeout=(10,60))
    try:
        j=r.json(); res=j.get("Resultados",[])
        return r.status_code, [(x.get("zona_carga"), len(x.get("Valores",[]))) for x in res]
    except Exception as e:
        return r.status_code, r.text[:100]

# variants for CENTRO ORIENTE
for label, z in [
    ("literal-space", "CENTRO ORIENTE"),
    ("plus", "CENTRO+ORIENTE"),
    ("pct20", "CENTRO%20ORIENTE"),
    ("nospace", "CENTROORIENTE"),
    ("underscore", "CENTRO_ORIENTE"),
]:
    print(label, vals(f"{base}/{z}/{date}"))
