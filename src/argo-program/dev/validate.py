import duckdb
import nodes.argo_program as M
from subsets_utils import raw_parquet_localpath


def run_transform(view_name, asset_id, transform_id):
    sql = [s.sql for s in M.TRANSFORM_SPECS if s.id == transform_id][0]
    with raw_parquet_localpath(asset_id) as p:
        con = duckdb.connect()
        con.execute(f"CREATE VIEW \"{view_name}\" AS SELECT * FROM read_parquet('{p}')")
        rows = con.execute(sql).fetch_arrow_table()
        print(f"  {transform_id}: {rows.num_rows} rows, cols={rows.column_names[:6]}...")
        print("  sample:", rows.slice(0, 1).to_pylist()[0] if rows.num_rows else None)


# --- ArgoFloats tiny window (6 hours) ---
cols = [n for n, _ in M.AF_COLS]
url = (M.ERDDAP + "/tabledap/ArgoFloats.csv?" + ",".join(cols)
       + "&time%3E=2024-06-01T00:00:00Z&time%3C=2024-06-01T06:00:00Z")
text = M._fetch_csv(url)
n = M._write_csv_parquet(text, M.AF_COLS, "dev-af-sample")
print(f"ArgoFloats sample parsed rows: {n}")
run_transform("argo-program-argofloats", "dev-af-sample", "argo-program-argofloats-transform")

# --- OACP grid (full, small) ---
M.fetch_grid("dev-oacp-sample")
run_transform("argo-program-oacp-argo-global", "dev-oacp-sample", "argo-program-oacp-argo-global-transform")

print("OK")
