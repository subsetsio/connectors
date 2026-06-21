from subsets_utils import get, get_client

SDMX = {"Accept":"application/vnd.sdmx.data+csv;version=1.0.0"}
flows404 = ["BBBK13","BBBK20","BBBP2","BBDG1","BBXP1"]

print("=== 404 flows: try wide ?format=csv and metadata ===")
for flow in flows404:
    # wide csv
    r = get(f"https://api.statistiken.bundesbank.de/rest/data/{flow}?format=csv", timeout=(15,120))
    print(f"{flow}: wide format={r.status_code} bytes={len(r.content) if r.status_code==200 else '-'}")

print()
print("=== check dataflow metadata for a 404 flow (BBBK13) ===")
r = get("https://api.statistiken.bundesbank.de/rest/metadata/dataflow/BBK/BBBK13", timeout=(15,120))
print("meta status", r.status_code, "len", len(r.content))
print(r.text[:600])

print()
print("=== BBKRT 413: try wide format, and SDMX-CSV with detail=dataonly ===")
for q in ["?format=csv", "?detail=dataonly", "?detail=serieskeysonly"]:
    try:
        client=get_client()
        with client.stream("GET", f"https://api.statistiken.bundesbank.de/rest/data/BBKRT{q}", headers=SDMX if 'detail' in q else None, timeout=(15,120)) as r:
            print(f"BBKRT {q}: status={r.status_code}")
    except Exception as e:
        print(f"BBKRT {q}: EXC {type(e).__name__} {str(e)[:60]}")
