import duckdb
import nodes.iom as m
from nodes.iom import (
    DTM_COLUMNS, MM_COLUMNS, MM_CSV_URL, MM_HEADERS,
    _http_get, _parse_csv, _resolve_dtm_csv_url,
)
import pyarrow as pa


def build_table(header, rows, colmap):
    idx = {h: i for i, h in enumerate(header)}
    schema = pa.schema([pa.field(n, pa.string()) for n in colmap.values()])
    cols = {}
    for src, name in colmap.items():
        i = idx[src]
        cols[name] = [(r[i] if i < len(r) and r[i] != "" else None) for r in rows]
    return pa.Table.from_pydict(cols, schema=schema)


con = duckdb.connect()

url = _resolve_dtm_csv_url()
h, r = _parse_csv(_http_get(url).content)
dtm = build_table(h, r, DTM_COLUMNS)
con.register("iom-dtm-displacement", dtm)
dtm_sql = next(s.sql for s in m.TRANSFORM_SPECS if s.id == "iom-dtm-displacement-transform")
dtm_t = con.execute(dtm_sql).fetch_arrow_table()
print("DTM raw rows:", dtm.num_rows, "| published rows:", dtm_t.num_rows)
print("DTM published schema:")
print(dtm_t.schema)

h2, r2 = _parse_csv(_http_get(MM_CSV_URL, headers=MM_HEADERS).content)
mm = build_table(h2, r2, MM_COLUMNS)
con.register("iom-missing-migrants", mm)
mm_sql = next(s.sql for s in m.TRANSFORM_SPECS if s.id == "iom-missing-migrants-transform")
mm_t = con.execute(mm_sql).fetch_arrow_table()
print("\nMM raw rows:", mm.num_rows, "| published rows:", mm_t.num_rows)
print("MM published schema:")
print(mm_t.schema)

print("\n--- sanity ---")
print("DTM admin_level distinct:", con.execute(f'SELECT DISTINCT admin_level FROM ({dtm_sql}) ORDER BY 1').fetchall())
print("DTM year range:", con.execute(f'SELECT min(year_reporting_date), max(year_reporting_date) FROM ({dtm_sql})').fetchall())
print("DTM min idp count:", con.execute(f'SELECT min(num_present_idp_ind) FROM ({dtm_sql})').fetchall())
print("MM year range:", con.execute(f'SELECT min(incident_year), max(incident_year) FROM ({mm_sql})').fetchall())
print("MM max incident_date:", con.execute(f'SELECT max(incident_date) FROM ({mm_sql})').fetchall())
print("MM main_id unique?:", con.execute(f'SELECT count(*)=count(DISTINCT main_id) FROM ({mm_sql})').fetchall())
print("MM min total_dead_and_missing:", con.execute(f'SELECT min(total_dead_and_missing) FROM ({mm_sql})').fetchall())
