from subsets_utils import get
BASE = "https://apidadosabertos.saude.gov.br"

def page_len(path, limit, offset, **extra):
    p = {"limit": limit, "offset": offset}; p.update(extra)
    r = get(BASE + path, params=p, timeout=(15.0, 180.0))
    try:
        d = r.json()
        if isinstance(d, dict):
            return r.status_code, next((len(v) for v in d.values() if isinstance(v, list)), None)
        if isinstance(d, list):
            return r.status_code, len(d)
        return r.status_code, None
    except Exception as e:
        return r.status_code, f"ERR {type(e).__name__}"

# max page size: ask for big limit on a large endpoint, see how many come back
print("--- max page size (SIM) ---")
for lim in (1000, 2000, 5000, 10000, 20000):
    print(f"  limit={lim}:", page_len("/vigilancia-e-meio-ambiente/sistema-de-informacao-sobre-mortalidade", lim, 0))

# rough total size via exponential offset probing
def estimate(path, **extra):
    lim = 1000
    # find an offset that returns empty
    off = 1000
    while True:
        st, n = page_len(path, 2, off, **extra)
        if n == 0 or isinstance(n, str):
            break
        off *= 4
        if off > 200_000_000:
            break
    print(f"  {path} {extra}: first-empty offset around {off} (status {st})")

print("--- size estimates (exp offset to first empty) ---")
estimate("/vigilancia-e-meio-ambiente/sistema-de-informacao-sobre-mortalidade")
estimate("/arboviroses/dengue", nu_ano=2023)
estimate("/vacinacao/doses-aplicadas-pni-2024")
estimate("/sisvan/estado-nutricional")
estimate("/cnes/estabelecimentos")
