import io
import pyarrow.parquet as pq
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from nodes.ookla import _list_partitions, _normalize, _download_parquet, _SOURCE_COLS, RAW_SCHEMA

parts = _list_partitions()
print("partition count:", len(parts))
types = sorted({p["type"] for p in parts})
years = sorted({p["year"] for p in parts})
print("types:", types, "years:", years)
print("sample:", parts[0], parts[-1])

# Take a recent partition (has centroid + loaded latency) and an old one, verify normalize.
recent = [p for p in parts if p["year"] == 2024 and p["quarter"] == 1 and p["type"] == "fixed"][0]
content = _download_parquet(recent["key"])
pf = pq.ParquetFile(io.BytesIO(content))
print("recent source cols:", pf.schema_arrow.names)
read_cols = [c for c in _SOURCE_COLS if c in pf.schema_arrow.names]
tbl = pf.read_row_group(0, columns=read_cols)
norm = _normalize(tbl, recent["type"], recent["year"], recent["quarter"])
print("normalized schema matches:", norm.schema.equals(RAW_SCHEMA))
print("rows:", norm.num_rows)
print(norm.slice(0, 1).to_pylist())
