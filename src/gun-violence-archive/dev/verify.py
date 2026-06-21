import sys, pyarrow as pa
sys.path.insert(0, "src")
import nodes.gun_violence_archive as m
from subsets_utils import configure_http
configure_http(headers={"User-Agent": m.BROWSER_UA})
rows = m._crawl_report("accidental-teen-deaths")
print("rows:", len(rows))
print("sample:", rows[0])
t = pa.Table.from_pylist(rows, schema=m.SCHEMA)
print("schema ok, table rows:", t.num_rows)
print("distinct ids:", len(set(r["incident_id"] for r in rows)))
