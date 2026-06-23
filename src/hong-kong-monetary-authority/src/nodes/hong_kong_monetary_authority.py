"""Hong Kong Monetary Authority — Open API connector.

Catalog connector over the HKMA Open API (https://api.hkma.gov.hk/public/). Each
of the 134 rank-active entities is one endpoint that returns a table with its own
column schema; we emit one download + one transform per entity.

Mechanism (from research): REST, no auth, JSON envelope `{header, result}` with
records in `result.records[]`. Pagination is offset/pagesize (max 1000); the
response carries no grand total, so we page until a short page is seen. Every
endpoint accepts `lang=en`. A handful of endpoints REQUIRE a `segment` parameter
and reject the request otherwise — the 1002 error message lists the valid segment
values in parentheses, which we parse and then fetch each segment, tagging rows
with a `_segment` column so the segment becomes a dimension on the published table.

Fetch shape: stateless full re-pull (shape 1). The whole corpus is small (largest
endpoints are a few thousand rows) and the API exposes no incremental filter we use
for snapshots, so each run re-pulls every endpoint in full and overwrites. Raw is
saved as NDJSON because schemas are heterogeneous across endpoints (and across
segments within an endpoint); the SQL transform re-types on read.
"""
import re

import pyarrow as pa  # noqa: F401  (kept available for future typed transforms)
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

from constants import ENTITY_IDS

SLUG = "hong-kong-monetary-authority"
BASE = "https://api.hkma.gov.hk/public/"
PAGE_SIZE = 1000
MAX_PAGES = 1000  # absolute safety ceiling per segment (~1M rows); raises if hit

# The 1002 error names the valid segment values, e.g.
# "segment is missing or invalid input (positions/turnover)".
_SEG_RE = re.compile(r"segment is missing or invalid input\s*\(([^)]+)\)", re.I)


@transient_retry()  # 6 attempts, exponential backoff on transient + 429 + 5xx
def _request(path: str, params: dict) -> dict:
    resp = get(BASE + path, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _detect_segments(path: str) -> list:
    """Return the list of required segment values, or [None] if the endpoint
    needs no segment. Raises on any other failure."""
    payload = _request(path, {"lang": "en", "pagesize": 1, "offset": 0})
    header = payload.get("header", {})
    if header.get("success"):
        return [None]
    msg = header.get("err_msg", "")
    m = _SEG_RE.search(msg)
    if m:
        return [s.strip() for s in m.group(1).split("/") if s.strip()]
    raise RuntimeError(f"{path}: unexpected API error: {msg}")


def _fetch_segment(path: str, segment) -> list:
    rows = []
    offset = 0
    for page in range(MAX_PAGES):
        params = {"lang": "en", "pagesize": PAGE_SIZE, "offset": offset}
        if segment is not None:
            params["segment"] = segment
        payload = _request(path, params)
        header = payload.get("header", {})
        if not header.get("success"):
            raise RuntimeError(
                f"{path} (segment={segment}, offset={offset}): "
                f"API error: {header.get('err_msg')}"
            )
        records = payload.get("result", {}).get("records", []) or []
        if segment is not None:
            for r in records:
                r["_segment"] = segment
        rows.extend(records)
        if len(records) < PAGE_SIZE:
            return rows
        offset += PAGE_SIZE
    raise RuntimeError(
        f"{path} (segment={segment}): exceeded MAX_PAGES={MAX_PAGES} — "
        "source grew past expectations; raise the cap deliberately."
    )


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = node_id[len(SLUG) + 1:]  # strip "hong-kong-monetary-authority-"
    path = entity_id.replace(".", "/")

    rows = []
    for segment in _detect_segments(path):
        rows.extend(_fetch_segment(path, segment))

    if not rows:
        raise RuntimeError(f"{asset}: endpoint {path} returned no records")

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per endpoint. Schemas are heterogeneous, so each
# transform is a straight typed pass-through over its NDJSON raw (DuckDB infers
# types per column). The 0-rows-fails-the-node rule is our correctness gate.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
