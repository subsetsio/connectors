import duckdb
from subsets_utils import get
B = "https://storage.googleapis.com/global-surface-water-stats"
for lvl in (3,4):
    r = get(f"{B}/hydrobasins{lvl}-all-2018.csv", timeout=(10,180))
    open(f"/tmp/hb{lvl}.csv","wb").write(r.content)
    print(f"hb{lvl} bytes", len(r.content))
con = duckdb.connect()
q = """
SELECT CAST(year AS INTEGER) AS year,
       CAST(PFAF_ID AS BIGINT) AS pfaf_id,
       LENGTH(CAST(PFAF_ID AS VARCHAR)) AS basin_level,
       CAST(permanent AS DOUBLE) AS permanent_sq_km
FROM read_csv_auto(['/tmp/hb3.csv','/tmp/hb4.csv'])
WHERE year IS NOT NULL AND PFAF_ID IS NOT NULL
"""
print("rowcount/levels:", con.execute("SELECT count(*), count(distinct basin_level), min(basin_level), max(basin_level) FROM ("+q+")").fetchall())
print("per-level rows:", con.execute("SELECT basin_level, count(*) FROM ("+q+") GROUP BY 1 ORDER BY 1").fetchall())
print("uniq (year,pfaf):", con.execute("SELECT count(*)=count(distinct (year,pfaf_id)) FROM ("+q+")").fetchall())
