import time
from subsets_utils import get

BASE = "https://transparency.entsog.eu/api/v1/"


def count(path, params):
    t0 = time.time()
    r = get(BASE + path, params=params, timeout=(10, 240))
    dt = time.time() - t0
    if r.status_code != 200:
        print(f"{path} {params} -> {r.status_code} {r.text[:80]}  ({dt:.1f}s)")
        return None
    d = r.json()
    rk = next((k for k in d if k != "meta" and isinstance(d[k], list)), None)
    n = len(d.get(rk, []))
    print(f"{path} {params} -> {n} rows  ({dt:.1f}s, ~{len(r.content)//1024}KB)")
    return n


# one full month of operationaldata at a big limit (size + timing)
count("operationaldata", {"from": "2024-01-01", "to": "2024-01-31", "limit": 50000})
count("operationaldata", {"from": "2024-01-01", "to": "2024-01-31", "limit": 50000, "offset": 50000})
count("operationaldata", {"from": "2024-01-01", "to": "2024-01-31", "limit": 1000000})

# full ~5y range counts for the smaller time-series (do they fit one asset?)
count("interruptions", {"from": "2021-07-01", "to": "2026-06-18", "limit": 1000000})
count("cmpUnavailables", {"from": "2021-07-01", "to": "2026-06-18", "limit": 1000000})
count("cmpUnsuccessfulRequests", {"from": "2021-07-01", "to": "2026-06-18", "limit": 1000000})
count("cmpAuctions", {"from": "2021-07-01", "to": "2026-06-18", "limit": 1000000})
