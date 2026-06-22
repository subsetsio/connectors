import sys; sys.path.insert(0, "src")
import duckdb, pyarrow.parquet as pq, pyarrow as pa
from nodes.australian_energy_market_operator import _parse_month, _fetch_csv, BASE_URL

# old 30-min file (no seconds) + recent 5-min
t98 = _parse_month(_fetch_csv(f"{BASE_URL}/PRICE_AND_DEMAND_199812_NSW1.csv"))
t26 = _parse_month(_fetch_csv(f"{BASE_URL}/PRICE_AND_DEMAND_202605_NSW1.csv"))
print("1998 rows", t98.num_rows, "dt0", t98.column('settlement_date')[0])
print("2026 rows", t26.num_rows, "dt0", t26.column('settlement_date')[0])
tbl = pa.concat_tables([t98, t26])
con = duckdb.connect()
con.register("australian-energy-market-operator-price-and-demand", tbl)
sql = open("src/nodes/australian_energy_market_operator.py").read()
# run the transform sql
q = '''SELECT region, settlement_date, total_demand, rrp, period_type
FROM "australian-energy-market-operator-price-and-demand"
WHERE region IS NOT NULL AND settlement_date IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY region, settlement_date ORDER BY total_demand DESC NULLS LAST)=1'''
r = con.execute(q).arrow()
print("transform rows", r.num_rows, "cols", r.column_names)
print("distinct (region,date)?", con.execute("SELECT count(*)-count(distinct (region||settlement_date::varchar)) FROM r").fetchone() if False else "skip")
