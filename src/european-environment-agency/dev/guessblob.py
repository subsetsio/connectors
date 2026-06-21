from subsets_utils import get
tests=[
 # statisticaldata no-blob, guess v5r1 (the version its sibling blobs use)
 "https://dis2datalake.blob.core.windows.net/discodata/statisticaldata/v5r1/eea_s_eu-sdg-06-30.zip",
 "https://dis2datalake.blob.core.windows.net/discodata/statisticaldata/latest/eea_s_eu-sdg-06-30.zip",
 # FISE no-blob guesses (need a version; try a couple)
 "https://dis2datalake.blob.core.windows.net/discodata/fise/latest/forest_countryfact.zip",
]
for u in tests:
    try:
        r=get(u, headers={"Range":"bytes=0-0"}, timeout=(10,60))
        print(r.status_code, r.headers.get("content-range"), u)
    except Exception as e:
        print("ERR", type(e).__name__, u)
