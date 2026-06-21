import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from subsets_utils import get

BASE = "https://hacker-news.firebaseio.com/v0"

def fetch(i):
    r = get(f"{BASE}/item/{i}.json", timeout=(10, 60))
    r.raise_for_status()
    return r.json()

# warm the shared client single-threaded first (as fetch_items does)
get(f"{BASE}/maxitem.json", timeout=(10, 60))

t0 = time.time()
ok = err = 0
errs = {}
with ThreadPoolExecutor(max_workers=64) as ex:
    futs = [ex.submit(fetch, i) for i in range(1, 5001)]
    for f in as_completed(futs):
        try:
            f.result()
            ok += 1
        except Exception as e:
            err += 1
            errs[type(e).__name__ + ":" + str(e)[:60]] = errs.get(type(e).__name__ + ":" + str(e)[:60], 0) + 1

print(f"ok={ok} err={err} in {time.time()-t0:.1f}s ({ok/(time.time()-t0):.0f}/s)")
for k, v in errs.items():
    print(f"  {v}x {k}")
