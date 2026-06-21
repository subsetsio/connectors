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


@transient_retry()
def _fetch_csv_text(url: str) -> str:
    # Read timeout is generous: the largest table (tariff measures) is a
    # ~300MB CSV streamed in one response.
    resp = get(url, params={"format": "csv"}, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.text


def _rows(text: str):
    # Free-text fields (descriptions, conditions) can be long; lift the field
    # size cap well above the default 128KB.
    csv.field_size_limit(1_000_000_000)
    yield from csv.DictReader(io.StringIO(text))


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataset, kind, source_id = FETCH_PARAMS[node_id]
    segment = "tables" if kind == "table" else "reports"
    url = f"{BASE}/v1/datasets/{dataset}/versions/latest/{segment}/{source_id}/data"
    text = _fetch_csv_text(url)
    # Stream rows into NDJSON (gzip) — one dict alive at a time, so the
    # multi-million-row tables never materialize as a full list/arrow table.
    save_raw_ndjson(_rows(text), asset, compression="gzip")


DOWNLOAD_SPECS = [
    NodeSpec(id=spec_id, fn=fetch_one, kind="download")
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
