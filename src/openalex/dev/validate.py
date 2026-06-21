"""Cheap local end-to-end check: real fetch logic -> arrow view -> transform SQL.
Does NOT write to the raw layer; uses a few partitions / one dimension only."""
import duckdb
import pyarrow as pa

import nodes.openalex as m


def run_sql(view_name, rows, sql):
    tbl = pa.Table.from_pylist(rows)
    con = duckdb.connect()
    con.register(view_name, tbl)
    out = con.execute(sql).arrow().read_all()
    return out


# --- reference: fields (tiny) + sdgs (tiny) ---
for ent in ["fields", "sdgs"]:
    rows = list(m._iter_entity_rows(ent))
    sid = f"openalex-{ent}"
    out = run_sql(sid, rows, m._REF_SQL[sid])
    print(f"\n=== {sid}: {len(rows)} raw rows -> {out.num_rows} transformed ===")
    print("cols:", out.column_names)
    print("sample:", out.slice(0, 1).to_pylist())

# --- works-by-year ---
rows = []
for g in m._works_group("publication_year"):
    k = str(g.get("key"))
    if k.isdigit():
        rows.append({"publication_year": int(k), "works_count": g.get("count")})
sql = next(s.sql for s in m.TRANSFORM_SPECS if s.id == "openalex-works-by-year-transform")
out = run_sql("openalex-works-by-year", rows, sql)
print(f"\n=== works-by-year: {len(rows)} raw -> {out.num_rows} rows, years "
      f"{out.column('publication_year').to_pylist()[:3]}...{out.column('publication_year').to_pylist()[-3:]} ===")

# --- works-by-dimension-year: ONE dimension only (sdg) to validate shape ---
dim, gb, filt = ("sdg", "sustainable_development_goals.id", "sustainable_development_goals.id")
drows = []
for v in m._works_group(gb):
    key, label = v.get("key"), v.get("key_display_name")
    for yg in m._works_group("publication_year", filt=f"{filt}:{key}"):
        yk = str(yg.get("key"))
        if yk.isdigit():
            drows.append({"dimension": dim, "dimension_key": m._short(key),
                          "dimension_label": label,
                          "publication_year": int(yk), "works_count": yg.get("count")})
sql = next(s.sql for s in m.TRANSFORM_SPECS if s.id == "openalex-works-by-dimension-year-transform")
out = run_sql("openalex-works-by-dimension-year", drows, sql)
print(f"\n=== works-by-dimension-year [sdg only]: {len(drows)} raw -> {out.num_rows} rows ===")
print("cols:", out.column_names)
print("sample:", out.slice(0, 2).to_pylist())
print("\nALL OK")
