import json
from subsets_utils import get

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}


def show(label, url, dig=None):
    print("=" * 70)
    print(label, url)
    try:
        r = get(url, headers=UA, timeout=(10, 120))
        print("status", r.status_code, "ctype", r.headers.get("content-type"))
        d = r.json()
        if dig:
            d = dig(d)
        if isinstance(d, list):
            print("LIST len", len(d))
            if d:
                print("first keys", sorted(d[0].keys()) if isinstance(d[0], dict) else type(d[0]))
                print("first:", json.dumps(d[0], indent=1)[:900])
        elif isinstance(d, dict):
            print("DICT keys", list(d.keys()))
            print(json.dumps(d, indent=1)[:900])
    except Exception as e:
        print("ERR", type(e).__name__, e)


# rates: search for full history (use a small window to inspect shape)
show("RATES secured search", "https://markets.newyorkfed.org/api/rates/secured/all/search.json?startDate=2026-06-01&endDate=2026-06-05", lambda d: d["refRates"])
show("RATES unsecured search", "https://markets.newyorkfed.org/api/rates/unsecured/all/search.json?startDate=2026-06-01&endDate=2026-06-05", lambda d: d["refRates"])
# tsy
show("TSY search summary", "https://markets.newyorkfed.org/api/tsy/all/results/summary/search.json?startDate=2024-01-01&endDate=2024-01-31", lambda d: d)
# ambs
show("AMBS search summary", "https://markets.newyorkfed.org/api/ambs/all/results/summary/search.json?startDate=2023-01-01&endDate=2023-03-31", lambda d: d)
# rp
show("RP search", "https://markets.newyorkfed.org/api/rp/all/all/results/search.json?startDate=2024-01-01&endDate=2024-01-10", lambda d: d)
# seclending
show("SECLENDING search summary", "https://markets.newyorkfed.org/api/seclending/all/results/summary/search.json?startDate=2024-01-01&endDate=2024-01-31", lambda d: d)
# fxs
show("FXS search", "https://markets.newyorkfed.org/api/fxs/all/search.json?startDate=2020-03-01&endDate=2020-06-30", lambda d: d)
# pd values bulk csv handled separately; pd get all timeseries json
show("PD get all timeseries", "https://markets.newyorkfed.org/api/pd/get/all/timeseries.json?startDate=2024-01-01&endDate=2024-01-31", lambda d: d)
# marketshare
show("MARKETSHARE qtrly latest", "https://markets.newyorkfed.org/api/marketshare/qtrly/latest.json", lambda d: d)
# soma summary
show("SOMA summary", "https://markets.newyorkfed.org/api/soma/summary.json", lambda d: d)
# soma holdings detail tsy
show("SOMA tsy holdings asof list", "https://markets.newyorkfed.org/api/soma/asofdates/list.json", lambda d: d)
