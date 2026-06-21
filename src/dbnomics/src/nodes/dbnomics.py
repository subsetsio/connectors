"""DBnomics connector — node module.

Source: DBnomics Web API v22 (chosen mechanism `rest_v22`, base
https://api.db.nomics.world/v22/, no auth). DBnomics is an aggregator of ~93
providers; each rank-accepted entity is ONE dataset (provider_code:dataset_code)
fetched in full from the series endpoint:

    GET /v22/series/{provider}/{dataset}?observations=1&limit=1000&offset=N

Each series doc carries parallel `period` / `period_start_day` / `value` arrays
(value "NA" => missing) plus a per-dataset `dimensions` map. We flatten to a
long table — one row per (series, period) — with a UNIFORM schema across every
dataset (the dataset's own dimensions are packed into a JSON `dimensions`
column so the raw shape is stable regardless of which dataset it is). The
series endpoint caps `limit` at 1000, so we page by offset until offset >=
num_found.

Scope (set in rank): flagship international / cross-country providers (IMF, BIS,
ECB, OECD, WB, WTO, ILO, FAO, AMECO, EC, major central banks, key US agencies)
at a feasible per-dataset size (2..10000 series, i.e. <=10 page requests). The
granular national statistical portals DBnomics also carries (CSO, Eurostat,
DESTATIS, ...) fan out into thousands of sub-datasets and have their own
dedicated connectors, so they are kept below the publish threshold.

Fetch shape: stateless full re-pull (shape 1) — each accepted dataset is small
enough to re-fetch entirely every run, so there is no watermark/cursor. The API
has no server-side `since`/`modifiedAfter` filter anyway (full corpus per
refresh); revisions are picked up for free. The entity id uses ':' between
provider and dataset (a path-safe separator; '/' would nest the published
table). The original entity id (and thus the real provider/dataset casing) is
recovered from the spec id via _SPEC_TO_ENTITY.
"""

import json

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)
from constants import ENTITY_IDS

BASE = "https://api.db.nomics.world/v22/series"
_PAGE = 1000

# spec id -> original collect entity id (preserves provider/dataset casing,
# which the case-sensitive series endpoint needs and which lower()ing the spec
# id would destroy).
_SPEC_TO_ENTITY = {
    f"dbnomics-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}


@transient_retry()
def _fetch_page(provider: str, dataset: str, offset: int) -> dict:
    resp = get(
        f"{BASE}/{provider}/{dataset}",
        params={"observations": 1, "limit": _PAGE, "offset": offset},
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return resp.json()


def _to_value(raw):
    if raw is None:
        return None
    if isinstance(raw, (int, float)):
        return float(raw)
    s = str(raw).strip()
    if s == "" or s.upper() == "NA":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _rows_from_doc(doc: dict):
    """One row per (series, period). Uniform schema across all datasets."""
    periods = doc.get("period") or []
    starts = doc.get("period_start_day") or []
    values = doc.get("value") or []
    dims = doc.get("dimensions") or {}
    dims_json = json.dumps(dims, ensure_ascii=False, sort_keys=True)
    series_code = doc.get("series_code")
    series_name = doc.get("series_name")
    frequency = doc.get("@frequency")
    provider_code = doc.get("provider_code")
    dataset_code = doc.get("dataset_code")
    for i, period in enumerate(periods):
        yield {
            "provider_code": provider_code,
            "dataset_code": dataset_code,
            "series_code": series_code,
            "series_name": series_name,
            "frequency": frequency,
            "period": period,
            "period_start_day": starts[i] if i < len(starts) else None,
            "value": _to_value(values[i] if i < len(values) else None),
            "dimensions": dims_json,
        }


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = _SPEC_TO_ENTITY[node_id]
    provider, _, dataset = entity_id.partition(":")

    rows = []
    offset = 0
    while True:
        payload = _fetch_page(provider, dataset, offset)
        series = payload.get("series", {})
        docs = series.get("docs", [])
        for doc in docs:
            rows.extend(_rows_from_doc(doc))
        num_found = series.get("num_found", 0)
        offset += _PAGE
        if offset >= num_found or not docs:
            break

    print(f"[dbnomics] {entity_id}: {len(rows)} observations")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"dbnomics-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One thin SQL transform per dataset: drop missing observations, cast the
# period start to a real date, and pass the uniform long schema through. Each
# dataset keeps its own dimensions in the JSON `dimensions` column.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                provider_code,
                dataset_code,
                series_code,
                series_name,
                frequency,
                period,
                TRY_CAST(period_start_day AS DATE) AS date,
                CAST(value AS DOUBLE)              AS value,
                dimensions
            FROM "{s.id}"
            WHERE value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
