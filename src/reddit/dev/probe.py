import time
from subsets_utils import get

API = "https://arctic-shift.photon-reddit.com/api"


def walk_count(floor):
    cursor = None
    seen = 0
    pages = 0
    t0 = time.time()
    while True:
        params = {"sort_type": "subscribers", "sort": "desc", "limit": 1000, "min_subscribers": floor}
        if cursor is not None:
            params["max_subscribers"] = cursor
        r = get(f"{API}/subreddits/search", params=params, timeout=(10, 120))
        data = r.json().get("data")
        if r.status_code != 200 or not data:
            break
        if cursor is not None:
            data = [d for d in data if d.get("subscribers") < cursor]
            if not data:
                break
        pages += 1
        seen += len(data)
        bottom = data[-1].get("subscribers")
        if bottom == cursor or bottom is None or bottom < floor:
            break
        cursor = bottom
        if pages > 200:
            break
    return seen, pages, time.time() - t0


for floor in (200000, 100000, 50000):
    n, p, dt = walk_count(floor)
    print(f"floor={floor}: ~{n} subreddits, {p} pages, {dt:.1f}s")
