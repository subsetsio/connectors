import json, re, sys
sys.path.insert(0, "src")
from subsets_utils import get

DCAT = "https://das-kba-statistikportal.hub.arcgis.com/api/feed/dcat-us/1.1.json"

def slug(s):
    return re.sub(r"-+","-", re.sub(r"[^a-z0-9]+","-", s.lower())).strip("-")

feed = get(DCAT, timeout=60).json()
m = {}
for ds in feed["dataset"]:
    title = ds.get("title","").strip()
    if not title: continue
    fs = None
    for d in ds.get("distribution",[]):
        if d.get("format")=="ArcGIS GeoServices REST API":
            fs = d.get("accessURL") or d.get("downloadURL")
    m[slug(title)] = fs

union = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/kraftfahrt-bundesamt/work/entity_union.json"))
print("union type:", type(union), "len:", len(union))
ids = union if isinstance(union, list) else list(union.keys() if isinstance(union, dict) else union)
print("first union entries:", ids[:3])
missing = [e for e in ids if e not in m]
print("union entities missing FS url:", missing)
print("total mapped:", len(m))

# probe date-bearing datasets
for s in ["fz-modellreihen", "fz-pkw-mit-elektroantrieb-bundesland", "fz-top50modellreihen"]:
    url = m[s]
    meta = get(url+"?f=json", timeout=45).json()
    dfields = [(f["name"], f["type"]) for f in meta["fields"]]
    print("\n===", s, "geom=", meta.get("geometryType"))
    print(" fields:", dfields)
    q = get(url+"/query", params={"where":"1=1","outFields":"*","returnGeometry":"false","resultRecordCount":2,"f":"json"}, timeout=45).json()
    feats = q.get("features",[])
    if feats:
        print(" sample attrs:", json.dumps(feats[0]["attributes"], ensure_ascii=False))
    print(" exceededTransferLimit:", q.get("exceededTransferLimit"))
