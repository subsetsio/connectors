from subsets_utils import get
BASE = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"

def try_json(url):
    r = get(url, timeout=(10, 120))
    try:
        return len(r.json()["periods"])
    except Exception:
        return f"FAIL({r.status_code},{r.text[:40]!r})"

# monthly span limit (series starts 1992)
for start in [2000, 1992, 1980, 1970, 1960, 1950, 1900]:
    print("monthly", start, "->", try_json(f"{BASE}/PN00001MM/json/{start}-1/2026-12"))

# daily series: find one with long history from metadata: TC interbancario PD04637PD
print("daily no-window ->", try_json(f"{BASE}/PD04637PD/json"))
for start in [2020, 2010, 2000, 1990]:
    print("daily", start, "->", try_json(f"{BASE}/PD04637PD/json/{start}-1-1/2026-12-31"))

# quarterly + annual format
print("quarterly ->", try_json(f"{BASE}/PN02526AQ/json/2000-1/2026-4"))
print("annual ->", try_json(f"{BASE}/PM05317AA/json/1950/2026"))
