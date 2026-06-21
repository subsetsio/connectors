import duckdb, pyarrow as pa
import sys
sys.path.insert(0, "src/nodes")
import joint_external_debt_hub as m

# fetch one series only
data = m._get_json(
    f"{m.BASE}/sources/{m.SOURCE_ID}/country/all/series/Q.5B0.5B0.C.5A.BKC.ASTT.1.ALL.MX.TO1.ALL/time/all",
    {"format": "json", "per_page": 500, "page": 1},
)
rows = m._parse_rows("Q.5B0.5B0.C.5A.BKC.ASTT.1.ALL.MX.TO1.ALL", data)
print("parsed rows:", len(rows), "| sample:", rows[0])
table = pa.Table.from_pylist(rows, schema=m.SCHEMA)

con = duckdb.connect()
con.register("joint-external-debt-hub-values", table)
sql = m.TRANSFORM_SPECS[0].sql
out = con.execute(sql).arrow().read_all()
print("transform out rows:", out.num_rows)
print("columns:", out.schema.names)
print(con.execute(sql + " LIMIT 3").df())
print("null period_start:", con.execute("SELECT count(*) FROM (" + sql + ") WHERE period_start IS NULL").fetchone())
