import json, re, sys
sys.path.insert(0, "src")
from subsets_utils import get

def slug(s):
    return re.sub(r"-+","-", re.sub(r"[^a-z0-9]+","-", s.lower())).strip("-")

feed = get("https://das-kba-statistikportal.hub.arcgis.com/api/feed/dcat-us/1.1.json", timeout=60).json()
m = {}
for ds in feed["dataset"]:
    title = ds.get("title","").strip()
    if not title: continue
    fs = None
    for d in ds.get("distribution",[]):
        if d.get("format")=="ArcGIS GeoServices REST API":
            fs = d.get("accessURL") or d.get("downloadURL")
    if fs: m[slug(title)] = fs

union = json.load(open("/Users/nathansnellaert/Documents/hardened/data/sources/kraftfahrt-bundesamt/work/entity_union.json"))
services = {e: m[e] for e in union}
assert len(services)==len(union), (len(services), len(union))

lines = []
lines.append('"""Catalog data for the KBA Statistikportal connector.')
lines.append("")
lines.append("ENTITY_IDS / SERVICES are the entity union (rank-accepted subsets) and the")
lines.append("slug -> ArcGIS FeatureServer-layer URL map, both copied verbatim from the")
lines.append("Hub DCAT feed at collect time. Data, not logic: kept out of the node module.")
lines.append('"""')
lines.append("")
lines.append("ENTITY_IDS = [")
for e in union: lines.append(f'    "{e}",')
lines.append("]")
lines.append("")
lines.append("# slug -> ArcGIS hosted FeatureServer layer 0 (query endpoint base)")
lines.append("SERVICES = {")
for e in union: lines.append(f'    "{e}": "{services[e]}",')
lines.append("}")
open("src/constants.py","w").write("\n".join(lines)+"\n")
print("wrote src/constants.py with", len(union), "entities")
print("sample:", union[0], "->", services[union[0]])
