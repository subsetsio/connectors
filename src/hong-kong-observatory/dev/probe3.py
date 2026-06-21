from subsets_utils import get
import json

BASE = "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php"

# RYES JSON for one recent date
r = get(BASE, params={"dataType": "RYES", "rformat": "json", "date": "20260615", "lang": "en"}, timeout=(10.0, 120.0))
print("RYES JSON status", r.status_code, "len", len(r.text))
try:
    d = r.json()
    print("type:", type(d))
    if isinstance(d, list):
        print("list len", len(d))
        print(json.dumps(d[0], indent=2, ensure_ascii=False)[:1500])
    elif isinstance(d, dict):
        print("keys:", list(d.keys())[:20])
        print(json.dumps(d, indent=2, ensure_ascii=False)[:1800])
except Exception as e:
    print("not json:", e)
    print(r.text[:800])

# RYES earliest date
print("\n--- RYES earliest probe ---")
for date in ("20190909", "20190910", "20190911"):
    rr = get(BASE, params={"dataType": "RYES", "rformat": "json", "date": date, "lang": "en"}, timeout=(10.0, 120.0))
    ok = "Please include valid" not in rr.text and len(rr.text) > 100
    print(date, rr.status_code, len(rr.text), "valid" if ok else "INVALID")

# CLM station validity check - probe a few from the documented list
print("\n--- CLMTEMP station validity ---")
for st in ("HKO", "HKA", "KP", "SHA", "TMS", "YCT", "SE1", "ZZZ"):
    rr = get(BASE, params={"dataType": "CLMTEMP", "rformat": "csv", "station": st}, timeout=(10.0, 120.0))
    ok = "Please include valid" not in rr.text and len(rr.text) > 200
    n = len(rr.text.splitlines())
    print(f"{st}: {'valid' if ok else 'INVALID'} lines={n}")
