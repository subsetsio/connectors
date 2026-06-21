import duckdb, tempfile, os
from subsets_utils import get
import pyarrow.parquet as pq
import pyarrow as pa

# SDMX CSV transform check (small flow)
txt = get("https://data.un.org/WS/rest/data/UNSD,DF_UNData_UNFCC/",
          headers={"Accept":"application/vnd.sdmx.data+csv;version=1.0.0"}, timeout=(10,180)).text
d = tempfile.mkdtemp()
csvp = os.path.join(d, "flow.csv")
open(csvp,"w").write(txt)
con = duckdb.connect()
con.execute(f"CREATE VIEW v AS SELECT * FROM read_csv_auto('{csvp}')")
q = '''SELECT * EXCLUDE (OBS_VALUE, DATAFLOW), TRY_CAST(OBS_VALUE AS DOUBLE) AS obs_value
       FROM v WHERE TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL'''
r = con.execute(q).fetchnumpy()
print("SDMX cols:", list(r.keys()))
print("SDMX rows:", len(r["obs_value"]))

# SDG parquet transform check (tiny synthetic)
t = pa.table({
  "series":["A"],"series_description":["d"],"goal":["1"],"target":["1.1"],
  "indicator":["1.1.1"],"geo_area_code":["2"],"geo_area_name":["Africa"],
  "time_period":pa.array([1990],pa.int32()),"value":["51.4"],"value_type":["Float"],"source":["WB"]})
pp = os.path.join(d,"sdg.parquet"); pq.write_table(t, pp)
con.execute(f"CREATE VIEW s AS SELECT * FROM read_parquet('{pp}')")
sq = '''SELECT series, series_description, goal, target, indicator, geo_area_code,
        geo_area_name, time_period AS year, TRY_CAST(value AS DOUBLE) AS value,
        value_type, source FROM s WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL AND time_period IS NOT NULL'''
r2 = con.execute(sq).fetchnumpy()
print("SDG cols:", list(r2.keys()), "rows:", len(r2["value"]))
