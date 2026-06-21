import time
from subsets_utils import get

# 1) Can the main data-api stream CSV directly (one request for the full combined dataset)?
uuid = "01edb62e-5c45-4f43-8c91-16cba21cbb74"
print("=== MAIN data-api CSV attempts ===")
for url in [
    f"https://data.cms.gov/data-api/v1/dataset/{uuid}/data?format=csv",
    f"https://data.cms.gov/data-api/v1/dataset/{uuid}/data.csv",
]:
    try:
        r = get(url, timeout=(10, 60))
        ct = r.headers.get("content-type")
        body = r.text[:200]
        print(f"{url}\n  -> {r.status_code} ct={ct} head={body!r}\n")
    except Exception as e:
        print(url, "ERR", e)

# 2) Provider metastore CSV download — one GET for the whole dataset
print("=== PROVIDER metastore CSV ===")
pid = "0127-af37"
item = get(f"https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items/{pid}?show-reference-ids", timeout=(10,60)).json()
for dist in item.get("distribution", []):
    dd = dist.get("data", dist)
    url = dd.get("downloadURL")
    print("  downloadURL:", url, "mediaType:", dd.get("mediaType"))
    if url:
        t=time.time()
        r = get(url, timeout=(10,120))
        print(f"    GET -> {r.status_code} bytes={len(r.content)} in {time.time()-t:.1f}s ct={r.headers.get('content-type')}")
        print("    head:", r.text[:160].replace(chr(10),' | '))

# 3) main per-dataset CSV download speed (moderate dataset) + does data.json have a clean primary CSV?
print("=== MAIN data.json distribution enumeration (one dataset) ===")
dj = get("https://data.cms.gov/data.json", timeout=(10,120)).json()
byid = {}
for d in dj.get("dataset", []):
    ident = d.get("identifier","")
    # identifier like https://data.cms.gov/data-api/v1/dataset/<uuid>/data-viewer
    if "/dataset/" in ident:
        u = ident.split("/dataset/")[1].split("/")[0]
        byid[u] = d
print("datasets indexed:", len(byid))
d = byid.get(uuid)
csvs = [dist for dist in d.get("distribution",[]) if (dist.get("mediaType")=="text/csv" or dist.get("format")=="CSV")]
print(f"dataset {uuid}: {len(csvs)} CSV distributions; titles:")
for dist in csvs[:8]:
    print("   ", dist.get("title"), "->", str(dist.get("downloadURL"))[:110])
