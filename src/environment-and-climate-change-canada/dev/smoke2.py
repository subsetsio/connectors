import sys; sys.path.insert(0,"src")
import os, time; os.environ.pop("CI",None)
from nodes.environment_and_climate_change_canada import fetch_one
from subsets_utils import load_raw_ndjson
for sid in ["environment-and-climate-change-canada-aqhi-observations-realtime"]:
    t=time.time(); fetch_one(sid); dt=time.time()-t
    rows=load_raw_ndjson(sid)
    print(f"{sid}: {len(rows)} rows in {dt:.1f}s; keys sample={sorted(rows[0].keys())[:6]}")
