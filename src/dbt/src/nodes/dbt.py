"""DBT (UK Department for Business and Trade) Data API connector.

Source: https://data.api.trade.gov.uk (v1), no auth.

Strategy — stateless full re-pull. Each download node fetches one table (or
report) in full from the per-entity data endpoint and saves it as NDJSON. The
API exposes a per-table data endpoint that returns the entire table in one
request (no pagination); `latest` 302-redirects to the newest concrete
version, so we always pull the current release and overwrite. There is no
incremental/`since` filter, and re-pulling the whole corpus is cheap (largest
table ~300MB CSV / ~2.9M rows), so no watermark/cursor state is kept.

Format note: the data endpoint serves CSV for every table, but parquet is NOT
generated for some tables (e.g. `measures`, `barriers` 404 with NoSuchKey), so
CSV is the only universally-available format. We do NOT hand the raw CSV to the
SQL transform: DuckDB's read_csv_auto sniffer mis-parses the free-text tables
(market barriers' multiline `summary` collapses the whole row into one column).
Instead the download parses the CSV with Python's RFC-4180 csv reader (which
handles quoted multiline fields) and re-emits NDJSON, which the transform reads
deterministically via read_json_auto. Values stay as strings — missing values
arrive from the source as the literal "#NA", so honest VARCHAR columns are the
right shape and downstream can cast.
"""

import csv
import io

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

from constants import FETCH_PARAMS

BASE = "https://data.api.trade.gov.uk"

# market-barriers' per-table CSV is structurally ragged: the source flattens
# nested objects (country_or_territory, sectors) into a variable number of
# columns, so rows have 12 or 14 fields against a 12-name header — positional
# CSV parsing silently corrupts ~44% of rows. The whole-dataset JSON for this
# dataset is clean and well-keyed, so barriers is fetched and flattened from
# JSON instead.
BARRIERS_SPEC = "dbt-market-barriers--barriers"


@transient_retry()
def _fetch_csv_text(url: str) -> str:
    # Read timeout is generous: the largest table (tariff measures) is a
    # ~300MB CSV streamed in one response.
    resp = get(url, params={"format": "csv"}, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.text


@transient_retry()
def _fetch_json(url: str):
    resp = get(url, params={"format": "json"}, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.json()


def _csv_rows(text: str):
    # Free-text fields (descriptions, conditions) can be long; lift the field
    # size cap well above the default 128KB.
    csv.field_size_limit(1_000_000_000)
    yield from csv.DictReader(io.StringIO(text))


def fetch_one(node_id: str) -> None:
    """Flat tabular tables/reports: per-table CSV → NDJSON."""
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataset, kind, source_id = FETCH_PARAMS[node_id]
    segment = "tables" if kind == "table" else "reports"
    url = f"{BASE}/v1/datasets/{dataset}/versions/latest/{segment}/{source_id}/data"
    text = _fetch_csv_text(url)
    # Stream rows into NDJSON (gzip) — one dict alive at a time, so the
    # multi-million-row tables never materialize as a full list/arrow table.
    save_raw_ndjson(_csv_rows(text), asset, compression="gzip")


def _flatten_barrier(b: dict) -> dict:
    cot = b.get("country_or_territory") or {}
    sectors = b.get("sectors") or []
    return {
        "id": b.get("id"),
        "title": b.get("title"),
        "summary": b.get("summary"),
        "is_resolved": b.get("is_resolved"),
        "status_date": b.get("status_date"),
        "country_or_territory_name": cot.get("name"),
        "country_or_territory_trading_bloc": cot.get("trading_bloc"),
        "caused_by_trading_bloc": b.get("caused_by_trading_bloc"),
        "trading_bloc": b.get("trading_bloc"),
        "location": b.get("location"),
        "sectors": ", ".join(s.get("name", "") for s in sectors) if sectors else None,
        "last_published_on": b.get("last_published_on"),
        "reported_on": b.get("reported_on"),
    }


def fetch_barriers(node_id: str) -> None:
    """Market access barriers: whole-dataset JSON → flatten → NDJSON."""
    asset = node_id
    dataset, _kind, _source_id = FETCH_PARAMS[node_id]
    url = f"{BASE}/v1/datasets/{dataset}/versions/latest/data"
    data = _fetch_json(url)
    rows = [_flatten_barrier(b) for b in data["barriers"]]
    save_raw_ndjson(rows, asset, compression="gzip")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=spec_id,
        fn=fetch_barriers if spec_id == BARRIERS_SPEC else fetch_one,
        kind="download",
    )
    for spec_id in FETCH_PARAMS
]

# One published Delta table per subset. The NDJSON raw is already the
# publishable shape (one row per source record); the transform is a thin
# pass-through that also serves as the correctness gate — a 0-row result fails
# the node, catching a silently-empty or reshaped download.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=[spec.id],
        sql=f'SELECT * FROM "{spec.id}"',
    )
    for spec in DOWNLOAD_SPECS
]
