import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
os.environ.pop("CI", None)  # local dev mode -> writes under data/dev
import duckdb
from nodes.pordata import fetch_one, _parse_indicator, _get_page, BASE
from constants import ENTITY_SLUGS
from subsets_utils import load_raw_ndjson

for eid in ["portugal-10", "portugal-130", "portugal-550"]:
    sid = "pordata-" + eid
    fetch_one(sid)
    rows = load_raw_ndjson(sid)
    print(f"{sid}: rows={len(rows)} sample={rows[0] if rows else None}")
    # run the transform SQL via duckdb over the saved ndjson
    con = duckdb.connect()
    # locate the raw file
    import glob
    cand = glob.glob(f"data/dev/**/{sid}*.ndjson*", recursive=True) + glob.glob(f"data/**/{sid}*.ndjson*", recursive=True)
    print("   raw files:", cand[:2])
    if cand:
        f = cand[0]
        rd = "read_ndjson_auto" 
        q = f'''SELECT CAST(indicator_id AS INTEGER) indicator_id, period,
                TRY_CAST(period AS INTEGER) year, series, series_group,
                CAST(value AS DOUBLE) value
                FROM {rd}('{f}') WHERE value IS NOT NULL AND series IS NOT NULL'''
        res = con.execute(q).fetchall()
        print(f"   transform rows={len(res)} first={res[0] if res else None}")
