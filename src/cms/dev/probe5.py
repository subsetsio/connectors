import time
from subsets_utils import get, get_client

# 1) huge main dataset via data.csv — stream, measure size + rows (cap the read so we don't pull GBs)
huge = "9552739e-3d05-4c1b-8eff-ecabf391e2e5"
url = f"https://data.cms.gov/data-api/v1/dataset/{huge}/data.csv"
print("=== HUGE main data.csv (streamed, first 50MB) ===")
client = get_client()
t = time.time()
nbytes = 0
nlines = 0
header = None
with client.stream("GET", url, timeout=30.0) as r:
    print("status", r.status_code, "ct", r.headers.get("content-type"), "len-header", r.headers.get("content-length"))
    for chunk in r.iter_bytes(chunk_size=1 << 20):
        nbytes += len(chunk)
        nlines += chunk.count(b"\n")
        if header is None:
            header = chunk.split(b"\n", 1)[0][:300]
        if nbytes > 50 * (1 << 20):
            break
print(f"read {nbytes/1e6:.1f} MB, ~{nlines} lines in {time.time()-t:.1f}s")
print("header:", header)

# 2) small main row-count sanity: data.csv full for 01edb62e should be 12120 data rows
url2 = "https://data.cms.gov/data-api/v1/dataset/01edb62e-5c45-4f43-8c91-16cba21cbb74/data.csv"
r = get(url2, timeout=(10, 120))
rows = r.text.count("\n")
print(f"\n01edb62e data.csv lines (incl header): {rows}  (expect ~12121)")

# 3) provider: direct datastore CSV download endpoint (avoid metastore lookup)?
print("\n=== PROVIDER datastore CSV download endpoint ===")
for url in [
    "https://data.cms.gov/provider-data/api/1/datastore/query/0127-af37/0/download?format=csv",
]:
    try:
        with client.stream("GET", url, timeout=30.0) as r:
            head = b""
            for chunk in r.iter_bytes(chunk_size=1 << 16):
                head = chunk[:200]; break
            print(url, "->", r.status_code, r.headers.get("content-type"), "head:", head[:160])
    except Exception as e:
        print(url, "ERR", e)
