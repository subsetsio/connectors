"""Probe: fetch SATCAT live, parse, and run the three transform SQLs in DuckDB."""
import sys
import csv
from io import StringIO

import duckdb
import pyarrow as pa

sys.path.insert(0, "/Users/nathansnellaert/Documents/hardened/connectors/src/celestrak/src")
sys.path.insert(0, "/Users/nathansnellaert/Documents/hardened/connectors/src/celestrak/src/nodes")
import celestrak as C  # noqa


text = C._fetch_satcat_text()
reader = csv.DictReader(StringIO(text))
rows = []
for r in reader:
    rows.append({
        "object_name": C._str(r.get("OBJECT_NAME")),
        "object_id": C._str(r.get("OBJECT_ID")),
        "norad_cat_id": C._int(r.get("NORAD_CAT_ID")),
        "object_type": C._str(r.get("OBJECT_TYPE")),
        "ops_status_code": C._str(r.get("OPS_STATUS_CODE")),
        "owner": C._str(r.get("OWNER")),
        "launch_date": C._str(r.get("LAUNCH_DATE")),
        "launch_site": C._str(r.get("LAUNCH_SITE")),
        "decay_date": C._str(r.get("DECAY_DATE")),
        "period": C._float(r.get("PERIOD")),
        "inclination": C._float(r.get("INCLINATION")),
        "apogee": C._float(r.get("APOGEE")),
        "perigee": C._float(r.get("PERIGEE")),
        "rcs": C._float(r.get("RCS")),
        "data_status_code": C._str(r.get("DATA_STATUS_CODE")),
        "orbit_center": C._str(r.get("ORBIT_CENTER")),
        "orbit_type": C._str(r.get("ORBIT_TYPE")),
    })

print(f"parsed {len(rows)} rows")
tbl = pa.Table.from_pylist(rows, schema=C.SCHEMA)

con = duckdb.connect()
for view in ("celestrak-satellite-catalog", "celestrak-launches-by-country", "celestrak-constellation-growth"):
    con.register(view, tbl)

for name, sql in [
    ("satellite-catalog", C._SATELLITE_CATALOG_SQL),
    ("launches-by-country", C._LAUNCHES_BY_COUNTRY_SQL),
    ("constellation-growth", C._CONSTELLATION_GROWTH_SQL),
]:
    res = con.execute(sql).arrow().combine_chunks() if False else con.execute(sql).fetch_arrow_table()
    print(f"\n=== {name}: {res.num_rows} rows, cols={res.column_names}")
    print(res.slice(0, 3).to_pylist())
    if name == "constellation-growth":
        consts = set(res.column("constellation").to_pylist())
        print("  constellations:", sorted(consts))
        starlink = [r for r in res.to_pylist() if r["constellation"] == "Starlink"]
        if starlink:
            print("  starlink max cumulative:", max(r["cumulative_total"] for r in starlink))
    if name == "launches-by-country":
        yrs = [int(r["year"]) for r in res.to_pylist() if r["year"]]
        print("  year range:", min(yrs), max(yrs))
