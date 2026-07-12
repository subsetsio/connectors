"""Fraser Institute — Economic Freedom datasets (efotw.org JSON API).

Three stateless full-pull download nodes, one per efotw.org endpoint. Each
endpoint returns its ENTIRE multi-year dataset in one GET as a JSON object keyed
by year string ("1970".."2023"); each year value is a list of jurisdiction
records carrying scalar fields plus Area1..AreaN sub-objects {label, value}.
Numeric values arrive as strings (some empty) and are cast in the transform.

The whole corpus is a few MB per endpoint with no incremental filter, so we
re-pull in full every run and overwrite — revisions and new report years (new
year keys) are picked up for free. No auth, no documented rate limit.
"""

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
)

_BASE = "https://www.efotw.org/api/v1/"

# download spec id -> efotw.org endpoint path
ENDPOINTS = {
    "fraser-institute-economic-freedom-of-the-world": "ftw_get_all_data",
    "fraser-institute-economic-freedom-of-north-america-allgov": "ftw_get_states_data",
    "fraser-institute-economic-freedom-of-north-america-subnational": "ftw_get_subnational_data",
}


@transient_retry()
def _fetch_json(path: str):
    resp = get(_BASE + path, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _flatten(payload: dict):
    """Year-keyed dict of record lists -> flat rows.

    Scalar fields are copied verbatim (kept as strings; cast downstream). Each
    Area sub-object {label, value} is flattened to its lowercased key holding the
    numeric string (e.g. "Area1" -> "area1", "Area1Rank" -> "area1rank"); labels
    are stable per dataset and live in the transform's column names instead.
    """
    rows = []
    for year_str, records in payload.items():
        year = int(year_str)
        for rec in records:
            row = {"year": year}
            for k, v in rec.items():
                if isinstance(v, dict):
                    row[k.lower()] = v.get("value")
                else:
                    row[k] = v
            rows.append(row)
    return rows


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    path = ENDPOINTS[node_id]
    payload = _fetch_json(path)
    rows = _flatten(payload)
    if not rows:
        raise AssertionError(f"{node_id}: endpoint {path} returned no records")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=spec_id, fn=fetch_one, kind="download") for spec_id in ENDPOINTS
]
