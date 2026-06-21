import sys, pathlib, io, json, gzip, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent/"src"))
import duckdb, pyarrow as pa, pyarrow.csv as pacsv, pyarrow.parquet as pq
from subsets_utils import get
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent/"src"/"nodes"))
import hm_land_registry as M

# --- PPD: build a small parquet, run the ppd transform SQL ---
r = get(M._PPD_YEAR_URL.format(year=2026), timeout=(10,120))
ro = pacsv.ReadOptions(column_names=M._PPD_COLS, autogenerate_column_names=False)
co = pacsv.ConvertOptions(column_types={c: pa.string() for c in M._PPD_COLS})
tbl = pacsv.read_csv(io.BytesIO(r.content), read_options=ro, convert_options=co)
pq.write_table(tbl, "/tmp/ppd.parquet")
sql = M.TRANSFORM_SPECS[0].sql.replace('"hm-land-registry-ppd"', "read_parquet('/tmp/ppd.parquet')")
out = duckdb.sql(sql).fetch_arrow_table()
print("PPD transform rows:", out.num_rows)
print("PPD cols:", out.column_names)
print("PPD sample:", {k: out.column(k)[0].as_py() for k in ["price","date_of_transfer","property_type","county"]})

# --- UKHPI: build small ndjson.gz for one region, run ukhpi transform SQL ---
rows=[]
for row in M._region_rows("england"):
    rows.append(row)
with gzip.open("/tmp/ukhpi.ndjson.gz","wt") as f:
    for row in rows:
        f.write(json.dumps(row)+"\n")
print("ukhpi england rows:", len(rows))
sql2 = M.TRANSFORM_SPECS[1].sql.replace('"hm-land-registry-ukhpi"', "read_json_auto('/tmp/ukhpi.ndjson.gz')")
out2 = duckdb.sql(sql2).fetch_arrow_table()
print("UKHPI transform rows:", out2.num_rows, "cols:", out2.num_columns)
print("UKHPI col sample:", out2.column_names[:8])
print("UKHPI sample:", {k: out2.column(k)[0].as_py() for k in ["region_slug","date","average_price","house_price_index","sales_volume"]})
