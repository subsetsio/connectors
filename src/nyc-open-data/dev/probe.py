import sys, tempfile
sys.path.insert(0, "src")
from subsets_utils.http_client import get_client
import duckdb

fxf = "tg4x-b46p"  # film permits, has CommunityBoard(s) etc.
url = f"https://data.cityofnewyork.us/api/views/{fxf}/rows.csv"
tmp = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
c = get_client()
with c.stream("GET", url, params={"$limit": 5000}, timeout=60) as resp:
    print("status", resp.status_code, "encoding", resp.headers.get("content-encoding"))
    for chunk in resp.iter_bytes():
        tmp.write(chunk)
tmp.close()
con = duckdb.connect()
rel = f"read_csv_auto('{tmp.name}', normalize_names=true, header=true)"
desc = con.execute(f"DESCRIBE SELECT * FROM {rel}").fetchall()
print("=== typed sniff columns ===")
for name, typ, *_ in desc:
    print(f"  {name!r}: {typ}")
n = con.execute(f"SELECT count(*) FROM {rel}").fetchone()[0]
print("rows:", n)
# all_varchar fallback shape
desc2 = con.execute(f"DESCRIBE SELECT * FROM read_csv_auto('{tmp.name}', normalize_names=true, header=true, all_varchar=true)").fetchall()
print("=== all_varchar names ===", [d[0] for d in desc2])
