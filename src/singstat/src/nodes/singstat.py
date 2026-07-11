"""SingStat (Singapore Department of Statistics) Table Builder connector.

Mechanism: REST. Strategy: stateless full re-pull - one fetch per table
(resourceId). The catalog is enumerated upstream (rank); here every accepted
resourceId gets one download spec that fetches its full table via
GET /api/table/tabledata/{resourceId}.

Each table's payload is row[].columns[] of period-to-value pairs across one or
more series (rowText). We flatten to one row per (series, period) with a
uniform schema: series_no, series_text, uom, period, value. Period formats are
heterogeneous across tables (annual "1960", quarterly "2024 1Q", monthly
"2024 Jan"), so period is kept as text.

No incremental query support upstream (no global since/cursor) - re-fetch the
full table each refresh; cheap, full content per request.
"""

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
)
from constants import ENTITY_IDS

BASE = "https://tablebuilder.singstat.gov.sg/api/table"

# The API 403s a bare/default User-Agent; a browser-like header set is accepted.
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

# All-string schema: the raw is faithful to the source (values like "na", "-",
# "s" are preserved as text); numeric coercion happens in compiled transforms.
SCHEMA = pa.schema([
    ("series_no", pa.string()),
    ("series_text", pa.string()),
    ("uom", pa.string()),
    ("period", pa.string()),
    ("value", pa.string()),
])


def _resource_id(node_id: str) -> str:
    """Recover the SingStat resourceId from a download node id.

    Spec ids are f"singstat-{entity_id.lower()}"; SingStat resourceIds are
    upper-case-letter-prefixed-or-numeric with no underscores/hyphens, so
    upper() reconstructs the original id exactly.
    """
    return node_id[len("singstat-"):].upper()


# tabledata hard-caps a response at 5000 (series,period) cells regardless of the
# `limit` value, so the full table must be paged via `offset` over the flattened
# cell stream until a short/empty page signals the end.
PAGE = 5000
MAX_PAGES = 2000  # ~10M cells; a runaway guard, not an expected limit


def _fetch_tabledata(resource_id: str, offset: int) -> dict:
    resp = get(
        f"{BASE}/tabledata/{resource_id}",
        params={"limit": PAGE, "offset": offset},
        headers=_HEADERS,
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    resource_id = _resource_id(node_id)

    rows = []
    offset = 0
    pages = 0
    while True:
        payload = _fetch_tabledata(resource_id, offset)
        data = payload.get("Data") or {}
        page_cells = 0
        for series in data.get("row", []):
            series_no = series.get("seriesNo")
            series_text = series.get("rowText")
            uom = series.get("uoM")
            for col in series.get("columns", []):
                rows.append({
                    "series_no": series_no,
                    "series_text": series_text,
                    "uom": uom,
                    "period": col.get("key"),
                    "value": col.get("value"),
                })
                page_cells += 1
        pages += 1
        if page_cells < PAGE:
            break
        offset += PAGE
        if pages >= MAX_PAGES:
            raise RuntimeError(
                f"{resource_id}: exceeded {MAX_PAGES} pages (>{MAX_PAGES * PAGE} "
                f"cells) - source larger than expected, refusing to truncate"
            )

    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"singstat-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
