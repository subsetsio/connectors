import io, zipfile, sys
import pyarrow as pa, pyarrow.csv as pacsv
import duckdb
sys.path.insert(0, "src")
from subsets_utils import get
from nodes.economic_policy_institute import COLUMNS, _transform_sql, _member_for, _member_indicator
from constants import INDICATOR_NAMES, CSV_FILENAMES

r = get("https://github.com/Economic/data/releases/latest/download/epi_swa_data_library.zip", timeout=(10,300))
zf = zipfile.ZipFile(io.BytesIO(r.content))

for eid in ["ceo_pay_ratio", "labor_force_unemp", "price_inflation", "minimum_wage_levels"]:
    member = _member_for(zf, eid)
    convert = pacsv.ConvertOptions(column_types={c: pa.string() for c in COLUMNS},
                                   null_values=[], strings_can_be_null=False)
    with zf.open(member) as fh:
        tbl = pacsv.read_csv(fh, pacsv.ReadOptions(), pacsv.ParseOptions(), convert).select(COLUMNS)
    con = duckdb.connect()
    con.register(f"economic-policy-institute-{eid.replace('_','-')}", tbl)
    dep = f"economic-policy-institute-{eid.replace('_','-')}"
    out = con.execute(_transform_sql(dep)).arrow()
    print(f"\n=== {eid} ({member}) raw_rows={tbl.num_rows} -> published_rows={out.num_rows}")
    print("  out cols:", out.column_names)
    print("  date range:", con.execute(f"SELECT min(date),max(date) FROM ({_transform_sql(dep)})").fetchall())
    print("  distinct measures:", con.execute(f"SELECT count(distinct measure) FROM ({_transform_sql(dep)})").fetchall())
    print("  sample:", out.slice(0,2).to_pylist())
