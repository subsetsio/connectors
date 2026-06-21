"""Coin Metrics Community API v4 connector.

Two published subsets, both daily (1d) long-format time series pulled from the
free community host (no API key):

  - asset-metrics       network/on-chain + market metrics across ~2300 assets
  - institution-metrics Grayscale trust metrics

Both are stateless full re-pulls: the community corpus is daily and modest, so
every run re-fetches the whole history and overwrites. Revisions/late
corrections are picked up for free (no stored watermark to trust). The
catalog-v2/* endpoints advertise which (asset, metric, 1d-frequency)
combinations are community==true; only those are fetched. timeseries/* returns
WIDE rows (one row per timestamp, one column per requested metric) whose column
set differs per asset, so each wide row is melted to uniform long records
(entity, metric, time, value) and written as parquet under one stable schema.
Large pulls are flushed in row-bounded batches to bound memory; the transform's
dep view glob-unions every batch automatically.
"""

import pyarrow as pa
from ratelimit import limits, sleep_and_retry

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://community-api.coinmetrics.io/v4"
FREQUENCY = "1d"
PAGE_SIZE = 10000
FLUSH_ROWS = 400_000          # melted long rows per parquet batch
MAX_PAGES_ABS = 100_000       # safety ceiling per series request

# Uniform long-format schema shared by every batch (entity column reused for
# both asset and institution — same physical layout, distinct logical key).
SCHEMA = pa.schema([
    ("entity", pa.string()),
    ("metric", pa.string()),
    ("time", pa.string()),     # ISO-8601 ns string; cast to TIMESTAMP in SQL
    ("value", pa.string()),    # numeric-as-string; cast to DOUBLE in SQL
    ("frequency", pa.string()),
])


@sleep_and_retry
@limits(calls=80, period=20)   # well under observed 6000/20s; honours headroom
@transient_retry()
def _fetch(url: str, params: dict | None = None) -> dict:
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _paginate(path: str, params: dict | None = None):
    """Yield every record across a cursor-paginated endpoint."""
    d = _fetch(f"{BASE}/{path}", params=params)
    yield from d.get("data", [])
    nxt = d.get("next_page_url")
    pages = 1
    while nxt:
        if pages >= MAX_PAGES_ABS:
            raise RuntimeError(f"pagination exceeded {MAX_PAGES_ABS} pages for {path}")
        d = _fetch(nxt)
        yield from d.get("data", [])
        nxt = d.get("next_page_url")
        pages += 1


def _community_metrics(catalog_path: str, key: str) -> dict[str, list[str]]:
    """Map each entity -> sorted community-available metrics at the 1d frequency."""
    out: dict[str, list[str]] = {}
    for rec in _paginate(catalog_path):
        ent = rec[key]
        metrics = sorted({
            m["metric"]
            for m in rec.get("metrics", [])
            for f in m.get("frequencies", [])
            if f.get("frequency") == FREQUENCY and f.get("community", True)
        })
        if metrics:
            out[ent] = metrics
    return out


def _melt(rows: list[dict], key_field: str):
    """Wide timeseries rows -> long (entity, metric, time, value) records."""
    for row in rows:
        ent = row.get(key_field)
        time = row.get("time")
        for k, v in row.items():
            if k in (key_field, "time") or v is None:
                continue
            yield {
                "entity": ent,
                "metric": k,
                "time": time,
                "value": str(v),
                "frequency": FREQUENCY,
            }


def _fetch_family(node_id: str, *, ts_path: str, catalog_path: str, key_field: str) -> None:
    """Generic driver: enumerate community metrics, pull each entity's full
    history, melt to long, flush row-bounded parquet batches."""
    metrics_by_entity = _community_metrics(catalog_path, key_field)
    if not metrics_by_entity:
        raise RuntimeError(f"{node_id}: catalog returned no community metrics")

    buf: list[dict] = []
    batch = 0

    def flush():
        nonlocal buf, batch
        if not buf:
            return
        table = pa.Table.from_pylist(buf, schema=SCHEMA)
        save_raw_parquet(table, f"{node_id}-{batch:05d}")
        batch += 1
        buf = []

    plural = key_field + "s"
    for entity, metrics in metrics_by_entity.items():
        params = {
            plural: entity,
            "metrics": ",".join(metrics),
            "frequency": FREQUENCY,
            "page_size": PAGE_SIZE,
        }
        wide = list(_paginate(ts_path, params))
        buf.extend(_melt(wide, key_field))
        if len(buf) >= FLUSH_ROWS:
            flush()
    flush()

    if batch == 0:
        raise RuntimeError(f"{node_id}: produced no rows")


def fetch_asset_metrics(node_id: str) -> None:
    _fetch_family(
        node_id,
        ts_path="timeseries/asset-metrics",
        catalog_path="catalog-v2/asset-metrics",
        key_field="asset",
    )


def fetch_institution_metrics(node_id: str) -> None:
    _fetch_family(
        node_id,
        ts_path="timeseries/institution-metrics",
        catalog_path="catalog-v2/institution-metrics",
        key_field="institution",
    )


DOWNLOAD_SPECS = [
    NodeSpec(id="coinmetrics-asset-metrics", fn=fetch_asset_metrics, kind="download"),
    NodeSpec(id="coinmetrics-institution-metrics", fn=fetch_institution_metrics, kind="download"),
]


def _transform_sql(download_id: str, key_alias: str) -> str:
    return f'''
        SELECT
            entity AS {key_alias},
            metric,
            CAST(time AS TIMESTAMP) AS time,
            CAST(value AS DOUBLE)   AS value,
            frequency
        FROM "{download_id}"
        WHERE value IS NOT NULL
          AND TRY_CAST(value AS DOUBLE) IS NOT NULL
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="coinmetrics-asset-metrics-transform",
        deps=["coinmetrics-asset-metrics"],
        sql=_transform_sql("coinmetrics-asset-metrics", "asset"),
    ),
    SqlNodeSpec(
        id="coinmetrics-institution-metrics-transform",
        deps=["coinmetrics-institution-metrics"],
        sql=_transform_sql("coinmetrics-institution-metrics", "institution"),
    ),
]
