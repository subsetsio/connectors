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

# DTM
url = _resolve_dtm_csv_url()
h, r = _parse_csv(_http_get(url).content)
dtm = build_table(h, r, DTM_COLUMNS)
print("DTM raw rows:", dtm.num_rows, "cols:", len(dtm.column_names))
con.register("iom-dtm-displacement", dtm)
dtm_sql = next(s.sql for s in m.TRANSFORM_SPECS if s.id == "iom-dtm-displacement-transform")
out = con.execute(dtm_sql).arrow()
print("DTM published rows:", out.num_rows)
print("DTM schema:", out.schema)

# MM
h2, r2 = _parse_csv(_http_get(MM_CSV_URL, headers=MM_HEADERS).content)
mm = build_table(h2, r2, MM_COLUMNS)
print("\nMM raw rows:", mm.num_rows, "cols:", len(mm.column_names))
con.register("iom-missing-migrants", mm)
mm_sql = next(s.sql for s in m.TRANSFORM_SPECS if s.id == "iom-missing-migrants-transform")
out2 = con.execute(mm_sql).arrow()
print("MM published rows:", out2.num_rows)
print("MM schema:", out2.schema)

# quick sanity probes
print("\nDTM admin_level distinct:", con.execute('SELECT DISTINCT admin_level FROM (' + dtm_sql + ') ORDER BY 1').fetchall())
print("DTM year range:", con.execute('SELECT min(year_reporting_date), max(year_reporting_date) FROM (' + dtm_sql + ')').fetchall())
print("MM year range:", con.execute('SELECT min(incident_year), max(incident_year) FROM (' + mm_sql + ')').fetchall())
print("MM max incident_date:", con.execute('SELECT max(incident_date) FROM (' + mm_sql + ')').fetchall())
print("MM main_id unique?:", con.execute('SELECT count(*)=count(DISTINCT main_id) FROM (' + mm_sql + ')').fetchall())
