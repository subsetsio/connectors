"""UIS values — long-format observations, one request per indicator, streamed.

The whole corpus is ~8.6M observations across ~5,000 indicators; the largest
single indicator holds ~21k records (well under the API's 100k-per-query cap),
so `values` is fetched one request per indicator and streamed to parquet in
flushed batches. No incremental filter exists on the API, so this is a full
re-pull every run.
"""
import pyarrow as pa
import pyarrow.parquet as pq
from subsets_utils import NodeSpec, raw_parquet_writer
from utils import SLUG, get_json, fetch_indicators_list

# Flush the values stream to a parquet row group every ~100k buffered rows so
# memory stays bounded regardless of corpus size.
VALUES_FLUSH_ROWS = 100_000

# Safety ceiling: a single /data/indicators query is capped at 100k records by
# the API; if any indicator ever returns at/over this, the response was
# truncated and the per-indicator strategy is no longer cap-safe — fail loudly.
RECORD_CAP = 100_000

_VALUES_SCHEMA = pa.schema([
    ("indicator_id", pa.string()),
    ("geo_unit", pa.string()),
    ("year", pa.int64()),
    ("value", pa.float64()),
    ("magnitude", pa.string()),
    ("qualifier", pa.string()),
])


def _flush(writer: "pq.ParquetWriter", buffer: list[dict]) -> None:
    if not buffer:
        return
    writer.write_table(pa.Table.from_pylist(buffer, schema=_VALUES_SCHEMA))
    buffer.clear()


def fetch_values(node_id: str) -> None:
    asset = node_id
    inds = fetch_indicators_list()
    codes = [i["indicatorCode"] for i in inds if i.get("indicatorCode")]
    if not codes:
        raise AssertionError("no indicator codes discovered for values fetch")

    buffer: list[dict] = []
    total = 0
    with raw_parquet_writer(asset, _VALUES_SCHEMA) as writer:
        for code in codes:
            data = get_json("data/indicators", params={"indicator": code})
            records = data.get("records") or []
            if len(records) >= RECORD_CAP:
                # Truncation: this indicator exceeds the API's per-query cap and
                # the per-indicator strategy silently lost rows. Fail loudly
                # rather than publish partial data.
                raise AssertionError(
                    f"indicator {code} returned {len(records)} records "
                    f">= cap {RECORD_CAP}; response truncated, needs splitting"
                )
            for r in records:
                v = r.get("value")
                buffer.append({
                    "indicator_id": r.get("indicatorId"),
                    "geo_unit": r.get("geoUnit"),
                    "year": r.get("year"),
                    "value": float(v) if v is not None else None,
                    "magnitude": r.get("magnitude"),
                    "qualifier": r.get("qualifier"),
                })
            total += len(records)
            if len(buffer) >= VALUES_FLUSH_ROWS:
                _flush(writer, buffer)
        _flush(writer, buffer)
    print(f"  -> {asset}: {total:,} observations across {len(codes):,} indicators")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-values", fn=fetch_values, kind="download"),
]
