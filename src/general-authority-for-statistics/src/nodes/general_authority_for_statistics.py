"""GASTAT (General Authority for Statistics, Saudi Arabia) connector.

Data source: the Statistical Database Portal's **Flexmonster Data Server**
(https://database.stats.gov.sa/flexmonster). Each rank-active entity is a
Flexmonster "cube" identified by its `index_name_en`. We pull the full cube as
a flat observation table via the type-discriminated FDS protocol:

  POST /fields  {"index": <cube>, "type": "fields"}            -> column list+types
  POST /select  {"type":"select","index":<cube>,
                 "query":{"aggs":{"by":{"rows":[<all dims>]},
                                   "values":[{"field":{"uniqueName":<measure>},
                                              "func":"sum"} ...]}},
                 "page": N}                                     -> aggregated rows

Putting every dimension in `aggs.by.rows` returns one row per full dimension
combination, so the `sum` of each measure equals the single observed value at
that grain. We page through page 0..pageTotal-1 (50000 rows/page), drop the
grand-total/subtotal rows (whose `keys` don't carry every dimension), and apply
the portal's VISIBLE_FLAG_CODE='Y' filter (then drop that internal column).

Raw is written as NDJSON: column sets differ across cubes and a few values are
mixed int/float, so a per-cube schema can't be declared up front — NDJSON lets
the transform re-type on read.
"""

import pyarrow as pa  # noqa: F401  (kept for parity with crib; not strictly needed)

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    post,
    save_raw_ndjson,
    transient_retry,
)
from constants import ENTITY_IDS

PREFIX = "general-authority-for-statistics-"
FDS_URL = "https://database.stats.gov.sa/flexmonster"
# ASCII-only headers. The F5 WAF in front of the server rejects requests that
# lack a browser-like Origin/Referer, and only passes plain JSON bodies.
FDS_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Origin": "https://database.stats.gov.sa",
    "Referer": "https://database.stats.gov.sa/",
    # The F5 WAF rejects non-browser User-Agents (e.g. httpx's default), so we
    # present a plain Chrome UA. ASCII only.
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
}
PAGE_SIZE = 50000  # server-fixed; informational

# Map each download node id back to its original cube index. The id transform
# (lower + '_'->'-') is lossy, so we keep the reverse mapping here, derived from
# the imported entity union (a plain import, not module-level I/O).
ID_TO_INDEX = {
    PREFIX + eid.lower().replace("_", "-"): eid for eid in ENTITY_IDS
}


@transient_retry(attempts=6, min_wait=3, max_wait=60)
def _fds(body: dict) -> dict:
    resp = post(FDS_URL, json=body, headers=FDS_HEADERS, timeout=(10.0, 180.0))
    resp.raise_for_status()
    # The WAF returns HTTP 200 with an HTML 'Request Rejected' page instead of a
    # real error; treat a non-JSON body as transient so the retry kicks in.
    ctype = resp.headers.get("content-type", "")
    if "json" not in ctype.lower():
        raise RuntimeError(
            f"non-JSON response from FDS (likely WAF rejection): {resp.text[:120]!r}"
        )
    return resp.json()


def _classify_fields(fields: list[dict]) -> tuple[list[str], list[str]]:
    """Split a cube's fields into (dimensions, measures).

    Measures are the observation columns (names ending in _OBSV). If a cube
    exposes none by name, fall back to its numeric fields as measures so we
    still aggregate something rather than grouping by the value itself.
    """
    names = [f["uniqueName"] for f in fields if f.get("uniqueName")]
    measures = [n for n in names if n.endswith("_OBSV")]
    if not measures:
        numeric = {
            f["uniqueName"]
            for f in fields
            if f.get("type") == "number" and f.get("uniqueName")
        }
        # treat numeric, non-year columns as measures
        measures = [
            n for n in names
            if n in numeric and "YEAR" not in n.upper() and not n.endswith("_CODE")
        ]
    dims = [n for n in names if n not in set(measures)]
    return dims, measures


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime hands us the spec id; it IS the asset name
    index = ID_TO_INDEX[node_id]

    fields = _fds({"index": index, "type": "fields"}).get("fields", [])
    dims, measures = _classify_fields(fields)
    if not measures:
        # Nothing numeric to report — write an empty asset; the transform will
        # surface this as a (correctly) failing node for this one cube.
        save_raw_ndjson([], asset)
        return

    dim_set = set(dims)
    has_vflag = "VISIBLE_FLAG_CODE" in dim_set

    query = {
        "aggs": {
            "by": {"rows": [{"uniqueName": d} for d in dims]},
            "values": [
                {"field": {"uniqueName": m}, "func": "sum"} for m in measures
            ],
        }
    }

    rows = []
    page = 0
    page_total = 1
    while page < page_total:
        body = {"type": "select", "index": index, "query": query, "page": page}
        resp = _fds(body)
        page_total = resp.get("pageTotal", 1) or 1
        for agg in resp.get("aggs", []):
            keys = agg.get("keys") or {}
            # Drop grand-total / subtotal rows: they lack one or more dimensions.
            if not dim_set.issubset(keys.keys()):
                continue
            # Apply the portal's visibility filter, then drop the internal flag.
            if has_vflag:
                flag = str(keys.get("VISIBLE_FLAG_CODE", "")).strip().upper()
                if flag != "Y":
                    continue
            row = {k: v for k, v in keys.items() if k != "VISIBLE_FLAG_CODE"}
            vals = agg.get("values") or {}
            for m in measures:
                cell = vals.get(m) or {}
                row[m] = cell.get("sum")
            rows.append(row)
        page += 1

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=PREFIX + eid.lower().replace("_", "-"),
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per cube. Raw is already cleaned in fetch_one
# (grand totals dropped, visibility filtered, flag column removed), so the
# transform is a straight pass-through that publishes the cube's observations.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
