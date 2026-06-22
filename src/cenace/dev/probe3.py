import urllib.parse, json
from subsets_utils import get

def show(label, url):
    r = get(url, timeout=(10,90))
    try:
        j = r.json()
        res = j.get("Resultados", [])
        keys = [list(x.keys()) for x in res[:1]]
        names = [x.get("clv_nodo") or x.get("zona_carga") or x.get("clv_zona_reserva") for x in res]
        n = sum(len(x.get("Valores",[])) for x in res)
        print(label, r.status_code, "groups=", len(res), "names=", names[:6], "vals=", n)
    except Exception as e:
        print(label, r.status_code, "non-json", r.text[:120], e)

# multi-node PML
show("PML 2 nodes", "https://ws01.cenace.gob.mx:8082/SWPML/SIM/SIN/MDA/01PLO-115,01AHU-115/2024/06/01/2024/06/03/JSON")
# PEND multi-zone incl space
z = urllib.parse.quote("AGUASCALIENTES,CENTRO ORIENTE")
show("PEND 2 zones (1 spaced)", f"https://ws01.cenace.gob.mx:8082/SWPEND/SIM/SIN/MDA/{z}/2024/06/01/2024/06/01/JSON")
# PEND single spaced zone alt: plus-encoded
show("PEND spaced +",  "https://ws01.cenace.gob.mx:8082/SWPEND/SIM/SIN/MDA/CENTRO%20ORIENTE/2024/06/01/2024/06/01/JSON")
# MTR recent (should be empty/204 if not published)
r = get("https://ws01.cenace.gob.mx:8082/SWPML/SIM/SIN/MTR/01PLO-115/2026/06/20/2026/06/20/JSON", timeout=(10,60))
print("MTR recent:", r.status_code, len(r.text), r.text[:80])
