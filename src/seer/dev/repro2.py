import sys, os, collections
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import nodes.seer as m
from subsets_utils import load_raw_ndjson
import duckdb, glob

for sid in ["seer-survival-long-term-trends", "seer-incidence-and-mortality-comparison-long-term-trends"]:
    m.fetch_one(sid)
    rows = load_raw_ndjson(sid)
    colsets = collections.Counter(tuple(sorted(r.keys())) for r in rows)
    print(f"\n{sid}: {len(rows)} rows; distinct column-sets: {len(colsets)}")
    for cs,n in colsets.most_common():
        print("   ", n, "rows:", cs)
    # try the duckdb transform on the actual raw file
    f = glob.glob(os.path.join("data","raw",f"{sid}.ndjson*")) or glob.glob(os.path.join("..","..","..","data","**",f"{sid}.ndjson*"),recursive=True)
    print("   raw file:", f[:1])
    if f:
        try:
            n = duckdb.sql(f"SELECT count(*) FROM read_json_auto('{f[0]}')").fetchone()[0]
            print("   duckdb read_json_auto rows:", n, "OK")
        except Exception as e:
            print("   duckdb ERROR:", str(e)[:200])
