import time
from subsets_utils import get
FDSN = "https://earthquake.usgs.gov/fdsnws/event/1"
# count endpoint
r = get(f"{FDSN}/count", params={"format":"text","starttime":"2024-01-01","endtime":"2024-02-01"}, timeout=(10,120))
print("count 2024-01:", r.status_code, r.text[:200])
r = get(f"{FDSN}/count", params={"format":"text","starttime":"1900-01-01","endtime":"2025-01-01"}, timeout=(10,300))
print("count all:", r.status_code, r.text[:200])
# csv sample
t=time.time()
r = get(f"{FDSN}/query", params={"format":"csv","starttime":"2024-01-01","endtime":"2024-01-02","limit":5}, timeout=(10,120))
print("csv time", time.time()-t)
print(r.text[:1200])
