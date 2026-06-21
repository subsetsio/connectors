from subsets_utils import get

urls = [
    "https://data.berkeleyearth.org/auto/Regional/TAVG/Text/united-states-TAVG-Trend.txt",
]
for u in urls:
    r = get(u, timeout=(10, 120))
    print("====", u, r.status_code, len(r.text), "bytes")
    lines = r.text.splitlines()
    print("total lines:", len(lines))
    for ln in lines[:80]:
        print(repr(ln[:170]))
    print("--- last 3 lines ---")
    for ln in lines[-3:]:
        print(repr(ln[:170]))
