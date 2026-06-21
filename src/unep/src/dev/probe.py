import io, duckdb
from subsets_utils import get
B = "https://storage.googleapis.com/global-surface-water-stats"

# 1) gaul0 small: inspect columns/types via duckdb read_csv_auto on bytes
r = get(B + "/gaul0-all-2018.csv", timeout=(10,120))
print("gaul0 status", r.status_code, "bytes", len(r.content))
con = duckdb.connect()
con.execute("CREATE TABLE g0 AS SELECT * FROM read_csv_auto(?)", [io.BytesIO(r.content)] if False else None) if False else None
# duckdb can't read BytesIO directly; write temp
open("/tmp/g0.csv","wb").write(r.content)
print(con.execute("DESCRIBE SELECT * FROM read_csv_auto('/tmp/g0.csv')").fetchall())
print("rows", con.execute("SELECT count(*), min(year), max(year), count(distinct ADM0_NAME) FROM read_csv_auto('/tmp/g0.csv')").fetchall())
print("sample", con.execute("SELECT year, ADM0_NAME, ADM0_CODE, permanent, \"5yr_Permanent\" FROM read_csv_auto('/tmp/g0.csv') LIMIT 3").fetchall())

# 2) PFAF_ID digit length per hydrobasins level (sample via Range header)
for lvl in (3,4,5,6):
    rr = get(f"{B}/hydrobasins{lvl}-all-2018.csv", headers={"Range":"bytes=0-20000"}, timeout=(10,120))
    txt = rr.content.decode("utf-8","replace")
    lines = txt.splitlines()
    hdr = lines[0]
    pfaf = set()
    for ln in lines[1:]:
        if not ln.strip(): continue
        cols = ln.split(",")
        pfaf.add(len(cols[1]))  # PFAF_ID is 2nd column
    print(f"hb{lvl}: header={hdr[:40]!r} pfaf_id digit-lengths seen={sorted(pfaf)}")
