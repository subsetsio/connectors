import json, io, tempfile, os
import duckdb
from subsets_utils import get

# Pull 2 pages to get a realistic mix of records
rows = []
for p in (1, 2):
    d = get("https://www.aurorasaurus.org/web-obs/list", params={"page": p, "page_size": 200}, timeout=(10, 120)).json()
    rows.extend(d["results"])
print("rows pulled:", len(rows))

# Write as ndjson to a temp file (mimic raw ndjson)
fd, path = tempfile.mkstemp(suffix=".ndjson")
with os.fdopen(fd, "w") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")

con = duckdb.connect()
con.execute(f"CREATE VIEW src AS SELECT * FROM read_json_auto('{path}', maximum_object_size=20000000)")
print("\ncolumns:", [c for c in con.execute("DESCRIBE src").fetchall()])

q = """
SELECT
  TRY_CAST(id AS BIGINT)                         AS report_id,
  CAST(timestamp AS TIMESTAMP)                   AS observed_at,
  TRY_CAST(location.latitude AS DOUBLE)          AS latitude,
  TRY_CAST(location.longitude AS DOUBLE)         AS longitude,
  address_country                                AS country,
  address_state                                  AS state,
  CAST(see_aurora AS BOOLEAN)                    AS saw_aurora,
  CAST(valid AS BOOLEAN)                         AS valid,
  CAST(verified AS BOOLEAN)                      AS verified,
  verified_type,
  sky,
  array_to_string(colors, ',')                   AS colors,
  array_to_string(types, ',')                    AS types,
  activities,
  height,
  TRY_CAST(time_start AS TIMESTAMP)              AS report_time_start,
  TRY_CAST(time_end AS TIMESTAMP)                AS report_time_end,
  comment
FROM src
WHERE id IS NOT NULL
"""
res = con.execute(q).fetch_arrow_table()
print("\nresult rows:", res.num_rows)
print("schema:\n", res.schema)
print("\nnull report_id count:", con.execute(f"SELECT count(*) FROM ({q}) WHERE report_id IS NULL").fetchone())
print("distinct report_id:", con.execute(f"SELECT count(DISTINCT report_id) FROM ({q})").fetchone())
print("\nsample 2 rows:")
print(con.execute(q + " LIMIT 2").fetchdf().to_string())
os.remove(path)
