import csv, gzip, io, re, sys
import duckdb, pyarrow as pa, pyarrow.parquet as pq
sys.path.insert(0, "src")
from subsets_utils import get

NCEI="https://www.ncei.noaa.gov"
def gt(url, enc=None):
    r=get(url, timeout=(10,300)); r.raise_for_status()
    if enc: r.encoding=enc
    return r.text
def gb(url):
    r=get(url, timeout=(10,300)); r.raise_for_status(); return r.content

def clean(v): return v if v not in (None,""," ") else None
def stbl(header, rows):
    cols={c:[] for c in header}; n=len(header)
    for row in rows:
        if len(row)!=n: row=(list(row)+[None]*n)[:n]
        for c,v in zip(header,row): cols[c].append(clean(v))
    return pa.table({c:pa.array(cols[c],pa.string()) for c in header})
def norm(h):
    out,seen=[],{}
    for i,c in enumerate(h):
        name=(c or "").strip() or f"col_{i}"
        if name in seen: seen[name]+=1; name=f"{name}_{seen[name]}"
        else: seen[name]=0
        out.append(name)
    return out

# storm-events: 1 year sample
t=gzip.decompress(gb(NCEI+"/pub/data/swdi/stormevents/csvfiles/StormEvents_details-ftp_v1.0_d2020_c20260323.csv.gz")).decode("latin-1")
r=csv.reader(io.StringIO(t)); h=next(r); se=stbl(h,r)
pq.write_table(se,"/tmp/se.parquet")
# ibtracs: last3years sample (same schema as ALL)
IB=["SID","SEASON","NUMBER","BASIN","SUBBASIN","NAME","ISO_TIME","NATURE","LAT","LON","WMO_WIND","WMO_PRES","DIST2LAND","LANDFALL","USA_WIND","USA_PRES","USA_SSHS"]
t=gt(NCEI+"/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.last3years.list.v04r01.csv")
r=csv.reader(io.StringIO(t)); hh=next(r); next(r)
idx={c:hh.index(c) for c in IB}
rows=[[clean(row[idx[c]]) if idx[c]<len(row) else None for c in IB] for row in r if row]
ib=pa.table({c:pa.array([rr[i] for rr in rows],pa.string()) for i,c in enumerate(IB)})
pq.write_table(ib,"/tmp/ib.parquet")
# rsi
files=sorted(x for x in re.findall(r'href="([^"]+)"', gt(NCEI+"/data/regional-snowfall-index/access/")) if re.match(r'regional-snowfall-index_c\d+\.csv$',x))
t=gt(NCEI+"/data/regional-snowfall-index/access/"+files[-1])
r=csv.reader(io.StringIO(t)); h=norm(next(r)); rsi=stbl(h,r)
pq.write_table(rsi,"/tmp/rsi.parquet")
# nesis
files=sorted(x for x in re.findall(r'href="([^"]+)"', gt(NCEI+"/data/northeast-snowfall-impact-scale/access/")) if x.endswith(".csv"))
t=gt(NCEI+"/data/northeast-snowfall-impact-scale/access/"+files[-1], enc="latin-1")
r=csv.reader(io.StringIO(t)); h=norm(next(r)); ne=stbl(h,r)
pq.write_table(ne,"/tmp/ne.parquet")
print("rawrows se,ib,rsi,ne =", se.num_rows, ib.num_rows, rsi.num_rows, ne.num_rows)

# import the real transform SQL from the node module
import importlib.util
spec=importlib.util.spec_from_file_location("noaa","src/nodes/noaa.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
SQL=mod._SQL

con=duckdb.connect()
con.execute("CREATE VIEW \"noaa-storm-events\" AS SELECT * FROM read_parquet('/tmp/se.parquet')")
con.execute("CREATE VIEW \"noaa-international-best-track-archive-for-climate-stewardship-ibtracs\" AS SELECT * FROM read_parquet('/tmp/ib.parquet')")
con.execute("CREATE VIEW \"noaa-regional-snowfall-index\" AS SELECT * FROM read_parquet('/tmp/rsi.parquet')")
con.execute("CREATE VIEW \"noaa-northeast-snowfall-impact-scale\" AS SELECT * FROM read_parquet('/tmp/ne.parquet')")
for sid,sql in SQL.items():
    res=con.execute(sql).fetch_arrow_table()
    print(f"\n=== {sid} -> {res.num_rows} rows, {res.num_columns} cols ===")
    print("cols:", res.schema.names)
    print(res.slice(0,2).to_pylist())
