import sys; sys.path.insert(0,'src')
import zipfile
import xml.etree.ElementTree as ET
from nodes.federal_reserve import _series_rows, _localname, SCHEMA
import pyarrow as pa, duckdb
rows=[]
with zipfile.ZipFile("/tmp/dsr.zip") as zf:
    name=[n for n in zf.namelist() if n.lower().endswith("_data.xml")][0]
    with zf.open(name) as fh:
        for ev,elem in ET.iterparse(fh, events=("end",)):
            if _localname(elem.tag)=="Series":
                rows+= list(_series_rows(elem,"DSR")); elem.clear()
t=pa.Table.from_pylist(rows, schema=SCHEMA)
con=duckdb.connect(); con.register("federal-reserve-dsr", t)
out=con.execute('''
  SELECT release, series_name, frequency, time_period,
         TRY_CAST(time_period AS DATE) AS date, obs_value AS value, obs_status
  FROM "federal-reserve-dsr" WHERE obs_value IS NOT NULL
''').fetch_arrow_table()
print("out rows:", out.num_rows, "| null dates:", out.column("date").null_count)
print(out.slice(0,2).to_pylist())
