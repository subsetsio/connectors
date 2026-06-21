import time
from subsets_utils import get
BASE = "https://api.ojp.gov/bjsdataset/v1/"

# high offset on large dataset (r4j4-fdwx ~6.3M rows)
for off in [1000000, 6000000]:
    t = time.time()
    r = get(f"{BASE}r4j4-fdwx.json", params={"$order": ":id", "$limit": 5, "$offset": off}, timeout=(10.0, 180.0))
    n = len(r.json()) if r.status_code == 200 else -1
    print(f"offset {off}: status {r.status_code} rows {n} secs {round(time.time()-t,1)} body {r.text[:120]!r}")
