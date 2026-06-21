import json, time, tempfile, os
import duckdb
import httpx
from subsets_utils import get
BASE="https://api.waterdata.usgs.gov/ogcapi/v0"

def fetch(coll, params, tries=12):
    for i in range(tries):
        r=get(f"{BASE}/collections/{coll}/items",params=params,timeout=(10,120))
        if r.status_code==200: return r.json()
        if r.status_code in (429,500,502,503,504):
            wait=min(8*(i+1),90); print(f"  {coll} {r.status_code}, wait {wait}s"); time.sleep(wait); continue
        r.raise_for_status()
    raise RuntimeError(f"{coll}: exhausted retries")

def stringify(v):
    if v is None: return None
    if isinstance(v,str): return v
    if isinstance(v,(list,dict)): return json.dumps(v,separators=(",",":"))
    return str(v)
def feature_row(f):
    props=f.get("properties") or {}
    row={k:stringify(v) for k,v in props.items()}
    g=f.get("geometry") or {}
    if g.get("type")=="Point":
        c=g.get("coordinates") or []
        if len(c)>=2:
            row["_lon"]=stringify(c[0]); row["_lat"]=stringify(c[1])
    if "id" not in row and f.get("id") is not None:
        row["id"]=stringify(f.get("id"))
    return row

colls=["monitoring-locations","combined-metadata","peaks","daily","continuous",
       "field-measurements","channel-measurements","time-series-metadata"]
tmpd=tempfile.mkdtemp()
geom={}
for coll in colls:
    j=fetch(coll,{"f":"json","limit":80})
    feats=j.get("features") or []
    rows=[feature_row(f) for f in feats]
    geom[coll]=any("_lat" in row for row in rows)
    with open(os.path.join(tmpd,f"usgs-{coll}.ndjson"),"w") as fh:
        for row in rows: fh.write(json.dumps(row)+"\n")
    print(f"{coll:24s} rows={len(rows)} has_geom={geom[coll]}")
    time.sleep(1.0)
print("TMPDIR",tmpd)
