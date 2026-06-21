import json
from subsets_utils import get

IDS = [
    "045273ed28ce4589be48edc75c611116",  # Fire HU Loss by Year v33
    "0e752a67c9d342599cd12f9ca15bceca",  # E5SubCountyData
    "7a040ca9fc594092aa86da996036095e",  # E5_2025v2
    "50a042556345443ab45d84716fadc43e",  # E5 Sub County List
    "cf9ee3a2956f4958b5eca26805717ce1",  # ADU Annual Changes
    "163d99a832d94a229e41c62dde35f96f",  # cities_pl94
]

for iid in IDS:
    item = get(f"https://www.arcgis.com/sharing/rest/content/items/{iid}",
               params={"f": "json"}, timeout=(10, 60)).json()
    svc = item.get("url")
    print("=" * 70)
    print(iid, "|", item.get("title"), "|", item.get("type"))
    print("service:", svc)
    if not svc:
        print("  NO URL")
        continue
    root = get(svc, params={"f": "json"}, timeout=(10, 60)).json()
    layers = root.get("layers") or []
    tables = root.get("tables") or []
    print("  layers:", [(l.get("id"), l.get("name")) for l in layers],
          "tables:", [(t.get("id"), t.get("name")) for t in tables])
    # pick first layer or table
    lid = (layers or tables)[0]["id"] if (layers or tables) else 0
    meta = get(f"{svc}/{lid}", params={"f": "json"}, timeout=(10, 60)).json()
    print("  layer", lid, "type:", meta.get("type"), "geom:", meta.get("geometryType"),
          "maxRec:", meta.get("maxRecordCount"))
    fields = [(f["name"], f["type"]) for f in (meta.get("fields") or [])]
    print("  fields:", fields[:25])
    # count + one row
    cnt = get(f"{svc}/{lid}/query",
              params={"where": "1=1", "returnCountOnly": "true", "f": "json"},
              timeout=(10, 60)).json()
    print("  count:", cnt.get("count"))
    q = get(f"{svc}/{lid}/query",
            params={"where": "1=1", "outFields": "*", "returnGeometry": "false",
                    "resultRecordCount": 2, "f": "json"}, timeout=(10, 60)).json()
    feats = q.get("features") or []
    print("  exceededTransferLimit:", q.get("exceededTransferLimit"))
    print("  sample attrs:", json.dumps(feats[0]["attributes"]) if feats else None)
