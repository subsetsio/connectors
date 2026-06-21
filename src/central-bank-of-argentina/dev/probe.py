import json
from subsets_utils import get, configure_http
import ssl, httpx
# Probe per-variable series pagination
def g(url, **params):
    r = get(url, params=params, timeout=(10.0,120.0))
    r.raise_for_status()
    return r.json()

# variable 1 = reservas, daily since 1996
d = g("https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias/1", desde="1990-01-01", hasta="2026-06-20", limit=1000, offset=0)
print("VALUES keys:", list(d.keys()))
print("metadata:", d["metadata"])
print("first result:", d["results"][0])
print("returned:", len(d["results"]))

# Cotizaciones per currency
c = g("https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Cotizaciones/USD", fechadesde="1990-01-01", fechahasta="2026-06-20", limit=1000, offset=0)
print("\nCOTIZ keys:", list(c.keys()))
print("cotiz metadata:", c.get("metadata"))
r = c["results"]
print("cotiz results type:", type(r))
if isinstance(r, list):
    print("cotiz first:", json.dumps(r[0], ensure_ascii=False))
    print("cotiz len:", len(r))
