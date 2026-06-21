import zipfile, tempfile, os, sys, collections
import pyarrow as pa, pyarrow.csv as pacsv
from subsets_utils import get_client
sys.path.insert(0,"src/nodes"); import climate_trace as ct
def dl(iso):
    url=ct.PKG_URL.format(gas=ct.GAS,iso3=iso); tmp=tempfile.NamedTemporaryFile(suffix=".zip",delete=False)
    with get_client().stream("GET",url,timeout=(10,120)) as r:
        r.raise_for_status()
        for c in r.iter_bytes(1<<20): tmp.write(c)
    tmp.close(); return tmp.name
p=dl("USA"); zf=zipfile.ZipFile(p)
gran=collections.Counter()
yr=collections.Counter()
n=0
for m in ct._members(zf,"_emissions_sources_"):
    with zf.open(m) as fh:
        rdr=pacsv.open_csv(fh, read_options=ct.ASSET_READ, convert_options=ct.ASSET_CONVERT)
        for b in rdr:
            t=pa.Table.from_batches([b])
            for g in t.column("temporal_granularity").to_pylist(): gran[g]+=1
            for s in t.column("start_time").to_pylist():
                if s: yr[s[:4]]+=1
            n+=t.num_rows
os.unlink(p)
print("USA source rows:", n)
print("temporal_granularity:", dict(gran))
print("by year:", dict(sorted(yr.items())))
