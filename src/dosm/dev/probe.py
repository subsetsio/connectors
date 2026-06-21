import io, pyarrow.parquet as pq
from subsets_utils import get
url="https://storage.dosm.gov.my/cpi/cpi_2d_core.parquet"
r=get(url, timeout=(10,120)); r.raise_for_status()
t=pq.read_table(io.BytesIO(r.content))
print("rows",t.num_rows)
print(t.schema)
print(t.slice(0,2).to_pylist())
# a storage.data.gov.my one
url2="https://storage.data.gov.my/environment/air_pollution.parquet"
r2=get(url2, timeout=(10,120)); r2.raise_for_status()
t2=pq.read_table(io.BytesIO(r2.content))
print("air rows",t2.num_rows, t2.schema.names)
