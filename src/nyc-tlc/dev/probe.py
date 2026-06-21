import io, pyarrow.parquet as pq
from subsets_utils import get

def schema_of(url):
    r = get(url, timeout=(10,120))
    r.raise_for_status()
    buf = io.BytesIO(r.content)
    pf = pq.ParquetFile(buf)
    sch = pf.schema_arrow
    return pf.metadata.num_rows, [(f.name, str(f.type)) for f in sch]

base = "https://d37ci6vzurychx.cloudfront.net/trip-data"
for url in [
    f"{base}/yellow_tripdata_2009-01.parquet",
    f"{base}/yellow_tripdata_2015-06.parquet",
    f"{base}/yellow_tripdata_2022-03.parquet",
    f"{base}/yellow_tripdata_2025-02.parquet",
]:
    n, cols = schema_of(url)
    print("===", url.split("/")[-1], "rows=", n)
    for c,t in cols: print("   ", c, t)
