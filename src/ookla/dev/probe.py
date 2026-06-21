import io
import xml.etree.ElementTree as ET
import pyarrow.parquet as pq
from subsets_utils import get

BASE = "https://ookla-open-data.s3.us-west-2.amazonaws.com"
NS = "{http://s3.amazonaws.com/doc/2006-03-01/}"


def list_prefix(prefix, delimiter="/"):
    params = {"list-type": "2", "prefix": prefix}
    if delimiter:
        params["delimiter"] = delimiter
    r = get(BASE + "/", params=params, timeout=(10, 60))
    r.raise_for_status()
    root = ET.fromstring(r.content)
    prefixes = [e.text for e in root.iter(NS + "CommonPrefixes") for e in [e.find(NS + "Prefix")]]
    keys = [(e.findtext(NS + "Key"), e.findtext(NS + "Size")) for e in root.iter(NS + "Contents")]
    truncated = root.findtext(NS + "IsTruncated")
    return prefixes, keys, truncated


# Top level: which types?
print("=== types ===")
pfx, keys, trunc = list_prefix("parquet/performance/")
print(pfx)

print("=== years for fixed ===")
pfx, keys, trunc = list_prefix("parquet/performance/type=fixed/")
print(pfx)

print("=== quarters/files for fixed 2019 ===")
pfx, keys, trunc = list_prefix("parquet/performance/type=fixed/year=2019/quarter=1/")
print("prefixes", pfx)
print("keys", keys, "truncated", trunc)

print("=== quarters for mobile 2024 ===")
pfx, keys, trunc = list_prefix("parquet/performance/type=mobile/year=2024/")
print(pfx)

# inspect schema of an early file (2019 q1 fixed) and a recent one
print("\n=== schema 2019 q1 fixed ===")
url = BASE + "/parquet/performance/type=fixed/year=2019/quarter=1/2019-01-01_performance_fixed_tiles.parquet"
r = get(url, timeout=(10, 300))
r.raise_for_status()
pf = pq.ParquetFile(io.BytesIO(r.content))
print("rows:", pf.metadata.num_rows, "bytes:", len(r.content))
print(pf.schema_arrow)
tbl = pf.read_row_group(0)
print(tbl.slice(0, 2).to_pylist())
