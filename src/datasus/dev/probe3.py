from subsets_utils import get
BASE = "https://apidadosabertos.saude.gov.br"

def n_at(path, offset, limit=1000, **extra):
    p = {"limit": limit, "offset": offset}; p.update(extra)
    r = get(BASE + path, params=p, timeout=(15.0, 180.0))
    try:
        d = r.json()
        n = next((len(v) for v in d.values() if isinstance(v, list)), None) if isinstance(d, dict) else len(d)
    except Exception as e:
        n = f"ERR {type(e).__name__}"
    return r.status_code, n

def bisect_total(path, hi=300_000_000, **extra):
    # find boundary where a full page (1000) stops being returned
    lo = 0
    # ensure hi is empty/short
    while True:
        st, n = n_at(path, hi, **extra)
        if isinstance(n, str):
            print(f"    [{path} {extra}] ERROR at offset {hi}: {n} (status {st}) -> deep-offset wall")
            hi = hi // 2
            if hi < 1000: return None
            continue
        if n == 1000:
            lo = hi; hi *= 2
            continue
        break
    while hi - lo > 1000:
        mid = (lo + hi) // 2
        st, n = n_at(path, mid, **extra)
        if isinstance(n, str):
            print(f"    wall at {mid}: {n}")
            hi = mid; continue
        if n == 1000: lo = mid
        else: hi = mid
    print(f"    [{path} {extra}] total ~ {lo}..{hi}")
    return hi

print("SISVAN:"); bisect_total("/sisvan/estado-nutricional")
print("PNI 2024:"); bisect_total("/vacinacao/doses-aplicadas-pni-2024")
print("SIM:"); bisect_total("/vigilancia-e-meio-ambiente/sistema-de-informacao-sobre-mortalidade")
print("dengue 2023:"); bisect_total("/arboviroses/dengue", nu_ano=2023)
print("SINASC:"); bisect_total("/vigilancia-e-meio-ambiente/sistema-de-informacao-sobre-nascidos-vivos")
