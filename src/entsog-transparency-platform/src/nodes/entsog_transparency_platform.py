"""ENTSOG Transparency Platform connector — EU gas TSO transparency reporting.

Source: the single public REST API at https://transparency.entsog.eu/api/v1
(no auth, offset pagination via limit/offset). Every endpoint returns the
envelope ``{"meta": {...}, "<endpoint>": [ {row}, ... ]}``; an empty result is
either HTTP 404 or a 200 carrying ``{"message": "No result found"}``.

Fetch strategy:

* The eleven reference / event catalogs (operators, connectionpoints,
  operatorpointdirections, balancingzones, interconnections,
  aggregateInterconnections, interruptions, cmpUnavailables,
  cmpUnsuccessfulRequests, tariffssimulations, urgentmarketmessages) are finite
  corpora the API serves in full WITHOUT a date filter. Stateless full re-pull
  every run (shape 1) — revisions are picked up for free.

* operationaldata is the large long-format time-series and is the one endpoint
  that must be windowed: unfiltered and multi-week windows make the gateway time
  out (502/504). It is crawled one calendar month per window and written as one
  NDJSON fragment per month. Re-pulling all of it every run would move ~30GB
  from a source whose terms forbid "usage that reduces the performance of the
  ENTSOG TP", so the crawl is incremental: a watermark records the last month
  completed and each run re-fetches a 45-day trailing window (OVERLAP_DAYS) so
  that provisional-to-confirmed revisions are never missed. Writing a fragment
  replaces only that month, leaving the other fragments intact.

Two properties of this API drove the code and are easy to get wrong:

* **A short page does NOT mean the last page.** `limit=20000` on a one-week
  window returns `count=986` while `offset=986` on the same query returns a
  further 668 rows. Paging therefore stops only on an *empty* page, never on
  `len(batch) < limit`.

* **`from`/`to` select records whose validity period OVERLAPS the window**, and
  `periodize=false` returns each record with its original period. A one-week
  query thus returns that week's daily flow rows plus long-validity capacity
  rows whose `periodFrom` may be years earlier. Those recur in every window they
  overlap; the composite `id` is stable, so the transform de-duplicates on it.

All values are stringified before the NDJSON write so every column reads back as
VARCHAR (read_json_auto unions columns across the fragment files); the compiled
transforms then cast the columns each subset actually publishes. Empty strings
become NULL: read_json_auto infers a temporal/numeric type from JSON *string*
values and then raises ConversionException if the column also holds "".
"""
import calendar
from datetime import date, datetime, timedelta, timezone

from subsets_utils import (
    NodeSpec,
    get,
    load_state,
    save_state,
    save_raw_ndjson,
    transient_retry,
)
from constants import ENTITIES, CATALOG_SUFFIXES, SOURCE_MIN_YEAR, SOURCE_MIN_MONTH

BASE = "https://transparency.entsog.eu/api/v1"
PREFIX = "entsog-transparency-platform-"
PAGE = 10000
STATE_VERSION = 1

# One publish period (daily gas day) plus ENTSOG's provisional->confirmed
# revision lag, rounded up generously: re-crawl the trailing 45 days each run.
OVERLAP_DAYS = 45

# Safety ceiling. No single endpoint/window approaches this many rows; if one
# does, the source has grown past expectations or paging is looping — raise
# loudly rather than silently truncate.
MAX_OFFSET = 5_000_000


@transient_retry(attempts=8, min_wait=4, max_wait=120)
def _get_page(endpoint: str, params: dict):
    """Fetch one page, returning the parsed envelope or None for an empty window.

    ENTSOG answers an empty window with 404, which is a normal "nothing here",
    not an error to retry or raise on. transient_retry covers 429/5xx/network;
    any other 4xx raises as permanent.
    """
    resp = get(f"{BASE}/{endpoint}", params=params, timeout=(10.0, 170.0))
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


def _fetch_all(endpoint: str, base_params: dict) -> list[dict]:
    """Page through one endpoint+window until the server returns an empty page.

    Stopping on a short page would silently truncate — see the module docstring.
    """
    rows: list[dict] = []
    offset = 0
    while True:
        payload = _get_page(endpoint, dict(base_params, limit=PAGE, offset=offset))
        if payload is None:
            break
        batch = payload.get(endpoint) or []
        if not batch:
            break
        rows.extend(batch)
        offset += len(batch)
        if offset > MAX_OFFSET:
            raise RuntimeError(
                f"{endpoint} {base_params}: exceeded MAX_OFFSET={MAX_OFFSET} "
                "— source larger than expected, refusing to silently truncate"
            )
    return rows


def _stringify(row: dict) -> dict:
    """Coerce every value to a string, mapping null AND empty-string to None."""
    return {k: (None if v is None or v == "" else str(v)) for k, v in row.items()}


def _months(sy: int, sm: int, ey: int, em: int):
    """Yield (year, month) from (sy, sm) through (ey, em) inclusive."""
    y, m = sy, sm
    while (y, m) <= (ey, em):
        yield y, m
        m += 1
        if m > 12:
            m, y = 1, y + 1


def fetch_catalog(node_id: str) -> None:
    """Stateless full re-pull of one un-windowed catalog endpoint."""
    endpoint = ENTITIES[node_id[len(PREFIX):]]
    rows = [_stringify(r) for r in _fetch_all(endpoint, {})]
    if not rows:
        raise RuntimeError(f"{endpoint}: returned no rows — refusing to publish an empty catalog")
    save_raw_ndjson(rows, node_id)


def fetch_operationaldata(node_id: str) -> None:
    """Crawl operationaldata month by month, one raw fragment per month.

    Resumes from the persisted watermark (the last month written), rewound by
    OVERLAP_DAYS so revised months are re-fetched. Raw is written before the
    watermark advances, so an interrupted run resumes without a hole.
    """
    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {}

    start = date(SOURCE_MIN_YEAR, SOURCE_MIN_MONTH, 1)
    watermark = state.get("watermark")
    if watermark:
        rewound = date.fromisoformat(watermark) - timedelta(days=OVERLAP_DAYS)
        start = max(start, rewound.replace(day=1))

    today = datetime.now(timezone.utc).date()
    for y, m in _months(start.year, start.month, today.year, today.month):
        last = calendar.monthrange(y, m)[1]
        rows = _fetch_all(
            "operationaldata",
            {"from": f"{y}-{m:02d}-01", "to": f"{y}-{m:02d}-{last:02d}"},
        )
        if rows:
            save_raw_ndjson(
                [_stringify(r) for r in rows], node_id, fragment=f"{y}-{m:02d}"
            )
        save_state(node_id, {
            "schema_version": STATE_VERSION,
            "watermark": f"{y}-{m:02d}-01",
            "last_success_at": datetime.now(timezone.utc).isoformat(),
        })


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}operationaldata", fn=fetch_operationaldata, kind="download"),
] + [
    NodeSpec(id=f"{PREFIX}{suffix}", fn=fetch_catalog, kind="download")
    for suffix in CATALOG_SUFFIXES
]
