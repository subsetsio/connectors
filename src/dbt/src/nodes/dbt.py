"""DBT (UK Department for Business and Trade) Data API connector.

Source: https://data.api.trade.gov.uk (v1), no auth.

Each download node fetches one accepted table or report in full from the
per-entity data endpoint and saves NDJSON. The API exposes the current release
through `latest`, which 302-redirects to the newest concrete version. There is
no incremental filter, so every run re-pulls the full accepted corpus.
"""

import csv
import io

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
)

from constants import FETCH_PARAMS

BASE = "https://data.api.trade.gov.uk"

# market-barriers' per-table CSV is structurally ragged for the primary
# barriers table: nested objects expand to a variable number of columns, so
# positional CSV parsing corrupts rows. The whole-dataset JSON is clean for
# that entity, so it is fetched and flattened from JSON instead.
BARRIERS_SPEC = "dbt-market-barriers--barriers"
QUOTA_DEFINITIONS_SPEC = "dbt-uk-tariff-2021-01-01--quota-definitions"


def _fetch_csv_text(url: str) -> str:
    # Read timeout is generous: the largest table (tariff measures) is a
    # ~300MB CSV streamed in one response.
    resp = get(url, params={"format": "csv"}, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.text


def _fetch_json(url: str):
    resp = get(url, params={"format": "json"}, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.json()


def _csv_rows(text: str):
    # Free-text fields (descriptions, conditions) can be long; lift the field
    # size cap well above the default 128KB.
    csv.field_size_limit(1_000_000_000)
    yield from csv.DictReader(io.StringIO(text))


def _quota_definition_rows(text: str):
    for row in _csv_rows(text):
        for col in ("validity_start", "validity_end"):
            if row.get(col) == "#NA":
                row[col] = None
        yield row


def fetch_one(node_id: str) -> None:
    """Flat tabular tables/reports: per-table CSV → NDJSON."""
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataset, kind, source_id = FETCH_PARAMS[node_id]
    segment = "tables" if kind == "table" else "reports"
    url = f"{BASE}/v1/datasets/{dataset}/versions/latest/{segment}/{source_id}/data"
    text = _fetch_csv_text(url)
    rows = (
        _quota_definition_rows(text)
        if node_id == QUOTA_DEFINITIONS_SPEC
        else _csv_rows(text)
    )
    # Stream rows into NDJSON (gzip) — one dict alive at a time, so the
    # multi-million-row tables never materialize as a full list/arrow table.
    save_raw_ndjson(rows, asset, compression="gzip")


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
