"""Coin Metrics connector — Community API v4 (no auth).

Two published subsets:

- `coin-metrics-asset-metrics-catalog` — the metric dictionary (one row per
  metric: code, name, description, category, unit, data_type ...). Reference
  data, joinable to the values table via the `metric` column.
- `coin-metrics-asset-metrics-values` — long-format daily time series: one row
  per (asset, metric, date). Covers every asset/metric pair the community tier
  exposes at daily (`1d`) frequency.

Shape: stateless full re-pull each run (community history is small enough to
re-fetch in full; the values pull streams straight to one parquet so revisions
and late corrections are picked up for free). The Community API caps at
10 requests / 6 seconds per IP, so both fetch fns share a ~80% rate limiter.
"""

import datetime as _dt

import pyarrow as pa
from ratelimit import limits, sleep_and_retry

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://community-api.coinmetrics.io/v4"
PAGE_SIZE = 10000
ASSET_BATCH = 120                 # assets per timeseries request (URL stays well under limits)
MAX_PAGES_ABS = 100_000           # runaway-pagination safety ceiling (raises, never silent-returns)

# Metrics excluded from the published values table:
#  - AssetCompletionTime / AssetEODCompletionTime: operational timestamps, not values.
#  - volume_reported_spot_usd_1d: exchange SELF-reported spot volume, which Coin
#    Metrics' own docs flag as wash-trading-contaminated. It carries physically
#    impossible values (>1e50 USD) and is the untrusted counterpart to the
#    pro-only trusted-volume metric — noise, not a clean statistical series.
SKIP_METRICS = {
    "AssetCompletionTime",
    "AssetEODCompletionTime",
    "volume_reported_spot_usd_1d",
}

# Metric-dictionary columns we keep from reference-data/asset-metrics.
DICT_FIELDS = [
    "metric", "full_name", "description", "product", "category",
    "subcategory", "unit", "data_type", "type", "display_name", "docs_url",
]

DICT_SCHEMA = pa.schema([(f, pa.string()) for f in DICT_FIELDS])

ASSETS_SCHEMA = pa.schema([
    ("asset", pa.string()),
    ("full_name", pa.string()),
])

VALUES_SCHEMA = pa.schema([
    ("asset", pa.string()),
    ("metric", pa.string()),
    ("date", pa.date32()),
    ("value", pa.float64()),
])


# --------------------------------------------------------------------------- #
# HTTP                                                                          #
# --------------------------------------------------------------------------- #
@sleep_and_retry
@limits(calls=8, period=6)              # ~80% of the documented 10 req / 6 s community limit
@transient_retry()                      # retries 429/5xx/transient network errors with backoff
def _get_json(url: str, params: dict | None = None) -> dict:
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _paginate(url: str, params: dict):
    """Yield each page's `data` list, following next_page_url to completion."""
    page = _get_json(url, params)
    pages = 0
    while True:
        pages += 1
        if pages > MAX_PAGES_ABS:
            raise RuntimeError(f"pagination exceeded {MAX_PAGES_ABS} pages at {url} — source grew unexpectedly")
        yield page.get("data", [])
        nxt = page.get("next_page_url")
        if not nxt:
            return
        page = _get_json(nxt)           # next_page_url already carries all params + cursor


def _parse_date(ts: str) -> _dt.date:
    # Coin Metrics daily timestamps look like "2026-06-21T00:00:00.000000000Z".
    return _dt.date(int(ts[0:4]), int(ts[5:7]), int(ts[8:10]))


# --------------------------------------------------------------------------- #
# Fetch: metric dictionary                                                      #
# --------------------------------------------------------------------------- #
def fetch_catalog(node_id: str) -> None:
    asset = node_id
    rows = []
    for data in _paginate(f"{BASE}/reference-data/asset-metrics", {"page_size": 1000}):
        for rec in data:
            rows.append({f: (rec.get(f) if rec.get(f) is not None else None) for f in DICT_FIELDS})
    table = pa.Table.from_pylist(rows, schema=DICT_SCHEMA)
    save_raw_parquet(table, asset)


# --------------------------------------------------------------------------- #
# Fetch: asset reference                                                        #
# --------------------------------------------------------------------------- #
def fetch_assets(node_id: str) -> None:
    data = _get_json(f"{BASE}/catalog/assets").get("data", [])
    rows = [
        {
            "asset": rec.get("asset"),
            "full_name": rec.get("full_name"),
        }
        for rec in data
    ]
    table = pa.Table.from_pylist(rows, schema=ASSETS_SCHEMA)
    save_raw_parquet(table, node_id)


# --------------------------------------------------------------------------- #
# Fetch: long-format daily values                                               #
# --------------------------------------------------------------------------- #
def _discover_daily_coverage() -> dict[str, list[str]]:
    """Map each community-1d metric -> sorted list of assets that expose it.

    The timeseries endpoint rejects (400/403) any request where a metric is not
    community-supported for one of the requested assets, so we must request each
    metric only against the assets that actually have it.
    """
    coverage: dict[str, set[str]] = {}
    for data in _paginate(f"{BASE}/catalog-v2/asset-metrics", {"page_size": 1000}):
        for a in data:
            asset_id = a["asset"]
            for m in a.get("metrics", []):
                code = m["metric"]
                if code in SKIP_METRICS:
                    continue
                for fr in m.get("frequencies", []):
                    if fr.get("community") and fr.get("frequency") == "1d":
                        coverage.setdefault(code, set()).add(asset_id)
    return {code: sorted(assets) for code, assets in sorted(coverage.items())}


def _melt_page(rows: list[dict], metrics: list[str]) -> pa.Table:
    out_asset, out_metric, out_date, out_value = [], [], [], []
    for r in rows:
        a = r.get("asset")
        t = r.get("time")
        if not a or not t:
            continue
        d = _parse_date(t)
        for code in metrics:
            v = r.get(code)
            if v is None:
                continue
            try:
                fv = float(v)
            except (TypeError, ValueError):
                continue          # non-numeric (e.g. a stray timestamp metric) — drop
            out_asset.append(a)
            out_metric.append(code)
            out_date.append(d)
            out_value.append(fv)
    return pa.table(
        {"asset": out_asset, "metric": out_metric, "date": out_date, "value": out_value},
        schema=VALUES_SCHEMA,
    )


def fetch_values(node_id: str) -> None:
    asset = node_id
    coverage = _discover_daily_coverage()
    if not coverage:
        raise RuntimeError("no community daily coverage discovered — catalog-v2 shape changed")

    with raw_parquet_writer(asset, VALUES_SCHEMA) as writer:
        for metric, assets in coverage.items():
            for i in range(0, len(assets), ASSET_BATCH):
                batch = assets[i:i + ASSET_BATCH]
                params = {
                    "assets": ",".join(batch),
                    "metrics": metric,
                    "frequency": "1d",
                    "page_size": PAGE_SIZE,
                }
                for data in _paginate(f"{BASE}/timeseries/asset-metrics", params):
                    if not data:
                        continue
                    tbl = _melt_page(data, [metric])
                    if tbl.num_rows:
                        writer.write_table(tbl)


# --------------------------------------------------------------------------- #
# DAG                                                                           #
# --------------------------------------------------------------------------- #
DOWNLOAD_SPECS = [
    NodeSpec(id="coin-metrics-asset-metrics-catalog", fn=fetch_catalog, kind="download"),
    NodeSpec(id="coin-metrics-asset-metrics-values", fn=fetch_values, kind="download"),
    NodeSpec(id="coin-metrics-assets", fn=fetch_assets, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="coin-metrics-asset-metrics-catalog-transform",
        deps=["coin-metrics-asset-metrics-catalog"],
        sql='''
            SELECT
                metric,
                full_name,
                description,
                product,
                category,
                subcategory,
                unit,
                data_type,
                type,
                display_name,
                docs_url
            FROM "coin-metrics-asset-metrics-catalog"
            WHERE metric IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="coin-metrics-asset-metrics-values-transform",
        deps=["coin-metrics-asset-metrics-values"],
        sql='''
            SELECT
                asset,
                metric,
                CAST(date AS DATE) AS date,
                value
            FROM (
                SELECT
                    asset, metric, date, value,
                    row_number() OVER (
                        PARTITION BY asset, metric, date ORDER BY value
                    ) AS rn
                FROM "coin-metrics-asset-metrics-values"
                WHERE value IS NOT NULL
            )
            WHERE rn = 1
        ''',
    ),
]
