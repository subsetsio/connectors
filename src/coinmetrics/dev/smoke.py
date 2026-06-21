"""Validate melt + transform SQL on a real (small) pull without writing raw."""
import duckdb
import pyarrow as pa
from nodes.coinmetrics import _community_metrics, _melt, _paginate, SCHEMA, _transform_sql

# institution family is tiny (grayscale only) — exercise end to end in memory
mbe = _community_metrics("catalog-v2/institution-metrics", "institution")
print("institutions:", list(mbe), "metric counts:", {k: len(v) for k, v in mbe.items()})

ent, metrics = next(iter(mbe.items()))
wide = list(_paginate("timeseries/institution-metrics", {
    "institutions": ent, "metrics": ",".join(metrics[:40]),
    "frequency": "1d", "page_size": 10000,
}))
long_rows = list(_melt(wide, "institution"))
print("wide rows:", len(wide), "-> long rows:", len(long_rows))
print("sample long:", long_rows[0])

tbl = pa.Table.from_pylist(long_rows, schema=SCHEMA)
con = duckdb.connect()
con.register("coinmetrics-institution-metrics", tbl)
sql = _transform_sql("coinmetrics-institution-metrics", "institution")
out = con.execute(sql).arrow()
print("transform output rows:", out.num_rows, "cols:", out.column_names)
print("types:", out.schema)
print("sample:", out.slice(0, 1).to_pylist())
