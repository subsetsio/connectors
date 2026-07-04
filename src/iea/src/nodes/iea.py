"""IEA Energy Statistics Data Browser connector.

Source: the free public JSON API behind the IEA Energy Statistics Data Browser
(https://api.iea.org). Each of the 73 indicators is a self-contained dataset
fetched in full from GET /stats/indicator/<INDICATOR_ID> — one request returns
the complete long-format time series for every country/region and every year
(no pagination, no auth).

Fetch shape: stateless full re-pull. Per-indicator payloads are small
(0.4-8.3 MB, ~2k-37k rows) so we re-fetch each indicator in full every run and
overwrite — revisions and late corrections are picked up for free. There is no
incremental query parameter on this API, so no watermark is possible or needed.

Raw format: NDJSON. The row schema is consistent in key SET across indicators,
but field *types* drift between indicators (e.g. `year` and `flowOrder` arrive
as strings for some indicators and integers for others, and `value` is int or
float and may be null). NDJSON avoids a brittle parquet schema; the transform
SQL re-types each field with explicit CASTs.
"""

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

API = "https://api.iea.org"

# Canonical row keys. The /stats/indicator payload always uses this key set,
# but flow-dimensioned indicators omit the product* fields entirely (and any
# field could go missing on a given indicator). We normalize every row to this
# fixed set so the raw NDJSON always exposes the same columns — otherwise a
# transform CASTing an absent column hits a DuckDB binder error.
CANON_KEYS = (
    "year", "short", "flow", "value", "flowLabel", "flowOrder", "units",
    "product", "productLabel", "productOrder", "seriesLabel", "country",
)

# Entity union — the 73 rank-active IEA indicators (case-sensitive source ids).
from constants import ENTITY_IDS


def _spec_id(entity_id: str) -> str:
    return f"iea-{entity_id.lower().replace('_', '-')}"


# Map the (lowercased) spec id back to the case-sensitive indicator id the API
# expects. Lowercasing is lossy, so the fetch fn recovers the real id here.
_INDICATOR_BY_SPEC = {_spec_id(eid): eid for eid in ENTITY_IDS}


@transient_retry()
def _fetch_indicator(indicator: str) -> list:
    # No countries param -> the full series for every country/region and year.
    resp = get(
        f"{API}/stats/indicator/{indicator}",
        timeout=(10.0, 180.0),
        headers={"Accept": "application/json"},
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    indicator = _INDICATOR_BY_SPEC[node_id]
    rows = _fetch_indicator(indicator)
    if not isinstance(rows, list) or not rows:
        raise AssertionError(
            f"{node_id}: expected a non-empty JSON array for indicator "
            f"{indicator!r}, got {type(rows).__name__} of len "
            f"{len(rows) if hasattr(rows, '__len__') else 'n/a'}"
        )
    # Normalize to the canonical key set so every indicator's NDJSON exposes
    # the same columns (missing fields -> null).
    norm = [{k: r.get(k) for k in CANON_KEYS} for r in rows]
    save_raw_ndjson(norm, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]
