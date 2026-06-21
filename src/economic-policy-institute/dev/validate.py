import io, zipfile, sys
import pyarrow as pa, pyarrow.csv as pacsv
import duckdb
sys.path.insert(0, "src")
from subsets_utils import get
from nodes.economic_policy_institute import COLUMNS, _transform_sql, _member_for
from constants import INDICATOR_NAMES

r = get("https://github.com/Economic/data/releases/latest/download/epi_swa_data_library.zip", timeout=(10,300))
zf = zipfile.ZipFile(io.BytesIO(r.content))

for eid in ["ceo_pay_ratio", "labor_force_unemp", "price_inflation", "minimum_wage_levels"]:
    member = _member_for(zf, eid)
    convert = pacsv.ConvertOptions(column_types={c: pa.string() for c in COLUMNS},
                                   null_values=[], strings_can_be_null=False)
    with zf.open(member) as fh:
        tbl = pacsv.read_csv(fh, pacsv.ReadOptions(), pacsv.ParseOptions(), convert).select(COLUMNS)
    dep = f"economic-policy-institute-{eid.replace('_','-')}"
    con = duckdb.connect()
    con.register(dep, tbl)
    sql = _transform_sql(dep)
    out = con.execute(f"SELECT count(*) n, min(date) mn, max(date) mx, count(distinct measure) nm FROM ({sql})").fetchall()[0]
    nullval = con.execute(f"SELECT count(*) FROM ({sql}) WHERE value IS NULL").fetchall()[0][0]
    print(f"=== {eid} ({member}) raw={tbl.num_rows} pub={out[0]} dates={out[1]}..{out[2]} measures={out[3]} nullvals={nullval}")
    print("   sample:", con.execute(f"SELECT * FROM ({sql}) LIMIT 1").fetchall())
