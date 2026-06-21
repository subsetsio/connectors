import json
from subsets_utils import get

BASE = "https://api.waterdata.usgs.gov/ogcapi/v0"

# 1. number matched for each collection via limit=1
for coll in ["monitoring-locations","daily","continuous","field-measurements",
             "channel-measurements","combined-metadata","time-series-metadata","peaks"]:
    try:
        r = get(f"{BASE}/collections/{coll}/items", params={"f":"json","limit":1}, timeout=(10,120))
        j = r.json()
        nm = j.get("numberMatched")
        feats = j.get("features",[])
        keys = sorted(feats[0].get("properties",{}).keys()) if feats else []
        print(f"{coll:28s} status={r.status_code} numberMatched={nm} nfeat={len(feats)}")
        print("   prop keys:", keys)
    except Exception as e:
        print(f"{coll}: ERROR {type(e).__name__}: {e}")
