import sys, pyarrow as pa, duckdb
sys.path.insert(0, "src")
import nodes.sea_around_us as m

def sample_rows(measure, dimension, region_type="rfmo", limit_regions=2):
    rows = []
    for rid, name in m._list_regions(region_type)[:limit_regions]:
        for s in m._fetch_series(region_type, measure, dimension, rid):
            for pair in (s.get("values") or []):
                if not pair or pair[0] is None or pair[1] is None:
                    continue
                rows.append({
                    "region_type": region_type, "region_id": rid, "region_name": name,
                    "category": s.get("key"), "scientific_name": s.get("scientific_name"),
                    "entity_id": str(s["entity_id"]) if s.get("entity_id") is not None else None,
                    "year": int(pair[0]), "value": float(pair[1]),
                })
    return pa.Table.from_pylist(rows, schema=m.CATCH_SCHEMA)

for measure, dim in [("tonnage", "taxon"), ("value", "sector")]:
    did = f"sea-around-us-catch-{measure}-by-{dim}"
    tbl = sample_rows(measure, dim)
    sql = m._catch_transform_sql(did, measure, dim)
    con = duckdb.connect()
    con.register("raw_tbl", tbl)
    con.execute(f'CREATE VIEW "{did}" AS SELECT * FROM raw_tbl')
    res = con.execute(sql).fetch_arrow_table()
    print(f"\n== {did}: raw {tbl.num_rows} -> transform {res.num_rows} rows")
    print("   cols:", res.column_names)
    print("   sample:", {k: res.column(k)[0].as_py() for k in res.column_names})
