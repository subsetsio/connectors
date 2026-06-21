import zipfile, tempfile, os, sys, time
import pyarrow as pa, pyarrow.csv as pacsv, pyarrow.compute as pc, duckdb
from subsets_utils import get_client
sys.path.insert(0,"src/nodes"); import climate_trace as ct
def dl(iso):
    url=ct.PKG_URL.format(gas=ct.GAS,iso3=iso); tmp=tempfile.NamedTemporaryFile(suffix=".zip",delete=False)
    with get_client().stream("GET",url,timeout=(10,300)) as r:
        r.raise_for_status()
        for c in r.iter_bytes(1<<20): tmp.write(c)
    tmp.close(); return tmp.name
t0=time.time(); p=dl("USA"); print(f"download USA: {time.time()-t0:.1f}s, {os.path.getsize(p)/1e6:.0f}MB")
zf=zipfile.ZipFile(p)
t1=time.time(); parts=[]; raw_rows=0
for m in ct._members(zf,"_emissions_sources_"):
    with zf.open(m) as fh:
        tbl=pacsv.read_csv(fh, read_options=ct.ASSET_READ, convert_options=ct.ASSET_CONVERT)
    raw_rows+=tbl.num_rows
    if tbl.num_rows: parts.append(ct._aggregate_member_to_annual(tbl))
os.unlink(p)
ae=pa.concat_tables(parts)
print(f"aggregate USA: {time.time()-t1:.1f}s  raw_monthly={raw_rows}  annual={ae.num_rows}")
print("schema match:", ae.schema.equals(ct.ASSET_EMISSIONS_SCHEMA))
# uniqueness of source_id,year
con=duckdb.connect(); con.register("ae",ae)
dup=con.execute("select count(*) c from (select source_id,year,count(*) n from ae group by 1,2 having n>1)").fetchone()[0]
print("dup (source_id,year) groups:", dup)
con.register("climate-trace-asset-emissions", ae)
out=con.execute(ct.TRANSFORM_SPECS[1].sql).fetch_arrow_table()
print("transform out rows:", out.num_rows, "cols:", out.column_names)
print(out.slice(0,1).to_pylist())
