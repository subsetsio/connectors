import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import pyarrow as pa
from nodes.cran_logs import (_get_json, _s, CRANLOGS, CRANDB, PACKAGES_SCHEMA,
    PKG_DOWNLOADS_SCHEMA, R_DOWNLOADS_SCHEMA)

# r_downloads small range -> build table
data = _get_json(f"{CRANLOGS}/downloads/daily/2024-01-01:2024-01-02/R")
rows=[{"day":d.get("day"),"os":d.get("os"),"version":d.get("version"),
       "downloads":int(d["downloads"]) if d.get("downloads") is not None else None}
      for o in data for d in (o.get("downloads") or [])]
print("r_downloads rows", len(rows), "->", pa.Table.from_pylist(rows, schema=R_DOWNLOADS_SCHEMA).num_rows)

# package_downloads batch flatten
data = _get_json(f"{CRANLOGS}/downloads/daily/2024-01-01:2024-01-02/ggplot2,dplyr")
rows=[{"package":o.get("package"),"day":d.get("day"),"downloads":int(d["downloads"])}
      for o in data for d in (o.get("downloads") or []) if d.get("downloads") is not None]
print("pkg_downloads rows", len(rows), "->", pa.Table.from_pylist(rows, schema=PKG_DOWNLOADS_SCHEMA).num_rows)

# packages: slice of crandb latest (2 records)
cat = _get_json(f"{CRANDB}/-/latest?limit=2")
prows=[]
for name,rec in cat.items():
    prows.append({"package":_s(rec.get("Package")) or name,"version":_s(rec.get("Version")),
        "title":_s(rec.get("Title")),"description":_s(rec.get("Description")),
        "license":_s(rec.get("License")),"maintainer":_s(rec.get("Maintainer")),
        "needs_compilation":_s(rec.get("NeedsCompilation")),
        "date_publication":_s(rec.get("Date/Publication")),"url":_s(rec.get("URL")),
        "bugreports":_s(rec.get("BugReports")),"repository":_s(rec.get("Repository"))})
t=pa.Table.from_pylist(prows, schema=PACKAGES_SCHEMA)
print("packages rows", t.num_rows, "cols", t.column_names)
print("OK")
