import sys; sys.path.insert(0,'src')
import io, zipfile
import xml.etree.ElementTree as ET
from nodes.federal_reserve import _series_rows, _localname, SCHEMA
import pyarrow as pa

# parse the local DSR zip we already downloaded
with open("/tmp/dsr.zip","rb") as f:
    zb=f.read()
rows=[]
with zipfile.ZipFile(io.BytesIO(zb)) as zf:
    name=[n for n in zf.namelist() if n.lower().endswith("_data.xml")][0]
    with zf.open(name) as fh:
        for ev,elem in ET.iterparse(fh, events=("end",)):
            if _localname(elem.tag)!="Series": continue
            for r in _series_rows(elem,"DSR"):
                rows.append(r)
            elem.clear()
print("rows:", len(rows))
print("sample:", rows[0])
print("descs present:", rows[0]["short_description"], "|", rows[0]["long_description"])
# build table to confirm schema coercion
t=pa.Table.from_pylist(rows, schema=SCHEMA)
print("table rows", t.num_rows, "cols", t.column_names)
print("non-null values:", t.column("obs_value").null_count, "nulls of", t.num_rows)
