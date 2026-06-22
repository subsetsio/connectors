import sys
sys.path.insert(0, "src")
import pyarrow as pa
import duckdb
from nodes.berkeley_earth import _fetch_text, _parse, _region_name, SCHEMA, S3_GLOBAL, AUTO_REGIONAL

rows = []
# global land+ocean
t = _fetch_text(S3_GLOBAL + "Land_and_Ocean_complete.txt")
rows += _parse(t, region_slug="global", region_name="Global", level="global", variable="TAVG", domain="land_and_ocean")
# global land TAVG
t = _fetch_text(S3_GLOBAL + "Complete_TAVG_complete.txt")
rows += _parse(t, region_slug="global", region_name="Global", level="global", variable="TAVG", domain="land")
# US TAVG
t = _fetch_text(AUTO_REGIONAL.format(var="TAVG", slug="united-states"))
nm = _region_name(t, "united-states")
print("parsed region name:", repr(nm))
rows += _parse(t, region_slug="united-states", region_name=nm, level="country", variable="TAVG", domain="land")
# a 404 variable maybe
t = _fetch_text(AUTO_REGIONAL.format(var="TMAX", slug="georgia-(state)"))
print("georgia-(state) TMAX:", "None" if t is None else f"{len(t)} bytes")

tbl = pa.Table.from_pylist(rows, schema=SCHEMA)
print("rows:", tbl.num_rows, "cols:", tbl.column_names)

con = duckdb.connect()
con.register("berkeley-earth-temperature-timeseries", tbl)
sql = open("src/nodes/berkeley_earth.py").read()
# extract the SQL between the triple quotes of TRANSFORM_SPECS
import re
m = re.search(r"sql='''(.*?)'''", sql, re.S)
out = con.execute(m.group(1)).fetch_arrow_table()
print("transform rows:", out.num_rows)
print("transform cols:", out.column_names)
print(con.execute(f'''SELECT date, region_slug, variable, domain, monthly_anomaly FROM ({m.group(1)}) ORDER BY date DESC LIMIT 3''').fetchall())
# uniqueness check
dup = con.execute(f'''SELECT count(*) - count(DISTINCT (region_slug,level,variable,domain,year,month)) FROM ({m.group(1)})''').fetchone()
print("dup count after transform:", dup)
