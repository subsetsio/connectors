import sys
sys.path.insert(0, "src")
sys.path.insert(0, "src/nodes")
import importlib
m = importlib.import_module("realclearpolitics")
# verify exports resolved
print("exports OK:", bool(m.DOWNLOAD_SPECS), bool(m.TRANSFORM_SPECS))
races = m._enumerate_races()
print("enumerated races:", len(races))
sample = list(races.items())[:2]
for rid, href in sample:
    print("race", rid, m._classify(href), href)
    d = m._race_json(rid)
    print("  json ok:", bool(d), "poll entries:", len(d.get("poll", [])) if d else 0)
