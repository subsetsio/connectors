"""Run each TRANSFORM_SPEC's SQL against locally-parsed download tables via DuckDB."""
import duckdb
import subsets_utils

captured = {}
def fake_save(table, asset_id):
    captured[asset_id] = table
subsets_utils.save_raw_parquet = fake_save
import nodes.philadelphia_fed as m
m.save_raw_parquet = fake_save

# parse all downloads
for spec in m.DOWNLOAD_SPECS:
    spec.fn(spec.id)

for t in m.TRANSFORM_SPECS:
    con = duckdb.connect()
    for dep in t.deps:
        con.register(dep, captured[dep])
    try:
        res = con.execute(t.sql).fetch_arrow_table()
        published = t.id.replace("-transform", "")
        status = "OK " if len(res) > 0 else "ZERO"
        print(f"{status} {published:55s} rows={len(res):>7,} cols={res.column_names}")
    except Exception as e:
        print(f"FAIL {t.id}: {type(e).__name__}: {e}")
    con.close()
