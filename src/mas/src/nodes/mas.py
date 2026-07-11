"""Monetary Authority of Singapore (MAS) statistics via the data.gov.sg API.

MAS publishes its monetary, banking, FX, government-debt and insurance
statistics on Singapore's national open-data portal (data.gov.sg). Each dataset
is a distinct table fetched the same way: the v2 list-rows endpoint with cursor
pagination. No auth, no documented rate limit.

Two raw shapes come back, and the fetch fn auto-detects which by the presence
of a `DataSeries` label column:
  - **Wide** (the vast majority): a `DataSeries` label column plus one column
    per time period ('2026Apr' monthly, '20261Q' quarterly, '2026' annual) —
    up to ~660 period columns. DuckDB's JSON reader collapses objects with
    >200 keys into a single MAP column, so wide rows are **unpivoted to long**
    (data_series, period_raw, value_raw) here in Python before saving raw. The
    compiled SQL transform then normalises the period and casts the value.
  - **Long**: already row-per-observation (e.g. date, value); the vault_id row
    index is dropped and the rest is saved as-is.

Transforms are NOT authored here — the model stage profiles this raw and
compiles the per-table transform (src/transforms/<table>.sql + .yml).

Fetch strategy: stateless full re-pull every run (the whole MAS corpus is a few
thousand rows per dataset, cheap to refetch; this picks up SingStat revisions
for free). No incremental filter is offered by list-rows anyway.
"""

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

_BASE = "https://api-production.data.gov.sg/v2/public/api/datasets"
_PAGE_LIMIT = 5000
_MAX_PAGES = 10000  # safety ceiling; raises on hit (pagination loop guard)

# The accept-accepted entity union: one MAS dataset id per published subset.
from constants import ENTITY_IDS


def _spec_id(dataset_id: str) -> str:
    return f"mas-{dataset_id.lower().replace('_', '-')}"


# Reverse map so the generic fetch fn recovers the dataset id from the spec id
# (dataset ids contain an underscore that the spec id turns into a dash).
_ID_BY_SPEC = {_spec_id(d): d for d in ENTITY_IDS}


# ── Download ──────────────────────────────────────────────────────────


@transient_retry()
def _get_page(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _fetch_all_rows(dataset_id: str) -> list:
    """Page the list-rows endpoint via its opaque cursor until exhausted."""
    rows = []
    url = f"{_BASE}/{dataset_id}/list-rows?limit={_PAGE_LIMIT}"
    pages = 0
    while url:
        data = _get_page(url).get("data", {})
        batch = data.get("rows", [])
        rows.extend(batch)
        nxt = data.get("links", {}).get("next")
        if nxt and batch:
            url = f"{_BASE}/{dataset_id}/list-rows?limit={_PAGE_LIMIT}&{nxt}"
        else:
            break
        pages += 1
        if pages > _MAX_PAGES:
            raise RuntimeError(
                f"{dataset_id}: exceeded {_MAX_PAGES} pages — pagination loop?"
            )
    return rows


def _unpivot(rows: list) -> list:
    """Wide -> long: (data_series, period_raw, value_raw), one row per cell.

    Values are kept as raw strings ('na'/'-'/'' included); the transform casts
    and nulls them. vault_id (a row index) is dropped.
    """
    out = []
    for row in rows:
        series = row.get("DataSeries")
        for key, val in row.items():
            if key in ("vault_id", "DataSeries"):
                continue
            out.append({
                "data_series": series,
                "period_raw": key,
                "value_raw": None if val is None else str(val),
            })
    return out


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataset_id = _ID_BY_SPEC[node_id]
    rows = _fetch_all_rows(dataset_id)
    if rows and "DataSeries" in rows[0]:
        records = _unpivot(rows)
    else:
        records = [{k: v for k, v in r.items() if k != "vault_id"} for r in rows]
    save_raw_ndjson(records, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(d), fn=fetch_one, kind="download")
    for d in ENTITY_IDS
]
