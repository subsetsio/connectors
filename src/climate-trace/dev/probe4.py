import io, zipfile, csv, tempfile, os
import pyarrow as pa, duckdb
from subsets_utils import get_client
import sys
sys.path.insert(0, "src/nodes")
import climate_trace as ct

# parse ABW only for both member types
def dl(iso):
    url=ct.PKG_URL.format(gas=ct.GAS, iso3=iso)
    tmp=tempfile.NamedTemporaryFile(suffix=".zip",delete=False)
    with get_client().stream("GET",url,timeout=(10,120)) as r:
        r.raise_for_status()
        for c in r.iter_bytes(1<<20): tmp.write(c)
    tmp.close(); return tmp.name

p=dl("ABW")
zf=zipfile.ZipFile(p)
# country emissions
cols=ct.COUNTRY_EMISSIONS_SCHEMA.names
rows=[]
for m in ct._members(zf,"_country_emissions_"):
    with zf.open(m) as fh:
        for r in csv.DictReader(io.TextIOWrapper(fh,encoding="utf-8")):
            rows.append({**{c:(r.get(c) or None) for c in cols},"emissions_quantity":ct._f(r.get("emissions_quantity"))})
ce=pa.Table.from_pylist(rows,schema=ct.COUNTRY_EMISSIONS_SCHEMA)
print("CE rows:",ce.num_rows)
# asset emissions
fc={"lat","lon","emissions_quantity","activity","emissions_factor","capacity","capacity_factor"}
sc=[c for c in ct.ASSET_EMISSIONS_SCHEMA.names if c not in fc]
arows=[]
for m in ct._members(zf,"_emissions_sources_"):
    with zf.open(m) as fh:
        for r in csv.DictReader(io.TextIOWrapper(fh,encoding="utf-8")):
            rec={c:(r.get(c) or None) for c in sc}
            for c in fc: rec[c]=ct._f(r.get(c))
            arows.append(rec)
ae=pa.Table.from_pylist(arows,schema=ct.ASSET_EMISSIONS_SCHEMA)
print("AE rows:",ae.num_rows)
os.unlink(p)

# run the transform SQL
con=duckdb.connect()
con.register("climate-trace-country-emissions", ce)
con.register("climate-trace-asset-emissions", ae)
ce_sql=ct.TRANSFORM_SPECS[0].sql
ae_sql=ct.TRANSFORM_SPECS[1].sql
ce_out=con.execute(ce_sql).arrow()
ae_out=con.execute(ae_sql).arrow()
print("\nCE transform out rows:",ce_out.num_rows,"cols:",ce_out.column_names)
print(ce_out.slice(0,2).to_pylist())
print("\nAE transform out rows:",ae_out.num_rows,"cols:",ae_out.column_names)
print(ae_out.slice(0,1).to_pylist())
