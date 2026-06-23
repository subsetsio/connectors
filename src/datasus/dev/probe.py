import json
from subsets_utils import get

BASE = "https://apidadosabertos.saude.gov.br"

def show(path, **params):
    p = {"limit": 5, "offset": 0}
    p.update(params)
    r = get(BASE + path, params=p, timeout=(10.0, 120.0))
    print("===", path, "params=", p, "->", r.status_code)
    try:
        d = r.json()
    except Exception as e:
        print("  not json:", repr(r.text[:200])); return
    if isinstance(d, dict):
        print("  top-level keys:", list(d.keys()))
        for k, v in d.items():
            if isinstance(v, list):
                print(f"  list key '{k}': len={len(v)}")
                if v:
                    print("   first record keys:", list(v[0].keys())[:25])
                    print("   first record sample:", json.dumps(v[0], ensure_ascii=False)[:400])
            else:
                print(f"  scalar key '{k}':", repr(v)[:120])
    elif isinstance(d, list):
        print("  top-level list len:", len(d))
        if d: print("   keys:", list(d[0].keys())[:25])

# small reference table
show("/cnes/tipounidades")
# large microdata
show("/vigilancia-e-meio-ambiente/sistema-de-informacao-sobre-mortalidade")
# disease w/ nu_ano param
show("/arboviroses/dengue", nu_ano=2023)
# a per-year family member
show("/vacinacao/doses-aplicadas-pni-2024")
# the underscore one
show("/prevencao-e-promocao/distribuicao_epi_insumo")
# deep offset behaviour on a big one
print("\n--- deep offset probe (SIM) ---")
for off in (0, 10000, 100000, 1000000):
    r = get(BASE + "/vigilancia-e-meio-ambiente/sistema-de-informacao-sobre-mortalidade",
            params={"limit": 2, "offset": off}, timeout=(10.0, 120.0))
    try:
        d = r.json()
        n = next((len(v) for v in d.values() if isinstance(v, list)), None) if isinstance(d, dict) else len(d)
    except Exception as e:
        n = f"ERR {e}"
    print(f"  offset={off}: status={r.status_code} returned={n}")
# max limit probe
print("\n--- max limit probe ---")
for lim in (1000, 5000, 10000):
    r = get(BASE + "/cnes/tipounidades", params={"limit": lim, "offset": 0}, timeout=(10.0, 120.0))
    try:
        d = r.json(); n = next((len(v) for v in d.values() if isinstance(v, list)), None)
    except Exception as e:
        n = f"ERR {e}"
    print(f"  limit={lim}: status={r.status_code} returned={n}")
