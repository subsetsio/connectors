from subsets_utils import get, post
API = "https://api.statbank.dk/v1"

def info(tid):
    r = get(f"{API}/tableinfo/{tid}", params={"format": "JSON"}, timeout=(10, 120))
    r.raise_for_status(); return r.json()

def size(tid):
    inf = info(tid)
    vcodes = [v["id"] for v in inf["variables"]]
    # estimate cells
    cells = 1
    for v in inf["variables"]:
        cells *= max(1, len(v["values"]))
    body = {"table": tid, "lang": "en", "format": "BULK",
            "variables": [{"code": c, "values": ["*"]} for c in vcodes]}
    r = post(f"{API}/data", json=body, timeout=(10, 600))
    r.raise_for_status()
    n = len(r.content)
    print(f"{tid:10s} cells~{cells:>12,} bytes={n:>12,} ({n/1e6:6.1f} MB)")

for tid in ["DNVPDKF","DNVPDKR2","DNIFHVEM","DNIFINVE","DNSUBOH","DNVP2","DNBOPM","DNIIP","DNVPEJER","DNPI"]:
    try:
        size(tid)
    except Exception as e:
        print(tid, "ERR", type(e).__name__, str(e)[:120])
