import json
from subsets_utils import get

BASE = "https://transparency.entsog.eu/api/v1/"


def probe(path, params, show_fields=False):
    r = get(BASE + path, params=params, timeout=(10, 120))
    print(f"\n=== {path} {params} -> HTTP {r.status_code} ===")
    try:
        doc = r.json()
    except Exception as e:
        print("non-json:", r.text[:300])
        return
    meta = doc.get("meta", {})
    print("meta:", {k: meta.get(k) for k in ("count", "total", "limit", "offset")})
    rk = next((k for k in doc if k != "meta" and isinstance(doc[k], list)), None)
    print("resource_key:", rk, "len:", len(doc.get(rk, [])) if rk else None)
    if show_fields and rk and doc[rk]:
        rec = doc[rk][0]
        print("sample fields:", list(rec.keys()))
        print("sample record:", json.dumps(rec, default=str)[:600])


# reference endpoints — full corpus size
probe("operators", {"limit": 1})
probe("operatorpointdirections", {"limit": 1})
probe("connectionpoints", {"limit": 1})
probe("interconnections", {"limit": 1})

# operationaldata — total over a single day, single indicator, and across all indicators
probe("operationaldata", {"limit": 1, "indicator": "Physical Flow", "from": "2024-01-01", "to": "2024-01-01"}, show_fields=True)
probe("operationaldata", {"limit": 1, "from": "2024-01-01", "to": "2024-01-01"})
probe("operationaldata", {"limit": 1, "indicator": "Physical Flow", "from": "2024-01-01", "to": "2024-01-07"})

# other time-series
probe("interruptions", {"limit": 1, "from": "2024-01-01", "to": "2024-01-31"}, show_fields=True)
probe("cmpUnavailables", {"limit": 1, "from": "2024-01-01", "to": "2024-12-31"})
probe("cmpUnsuccessfulRequests", {"limit": 1, "from": "2024-01-01", "to": "2024-12-31"})
probe("cmpAuctions", {"limit": 1, "from": "2024-01-01", "to": "2024-12-31"}, show_fields=True)
probe("aggregatedData", {"limit": 1, "from": "2024-01-01", "to": "2024-01-31"}, show_fields=True)

# messages + tariffs
probe("urgentmarketmessages", {"limit": 1}, show_fields=True)
probe("tariffssimulations", {"limit": 1}, show_fields=True)
probe("tariffsfulls", {"limit": 1}, show_fields=True)
