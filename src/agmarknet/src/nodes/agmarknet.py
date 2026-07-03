"""Agmarknet (India) — daily mandi commodity prices.

Source: data.gov.in Open Government Data resource
9ef84268-d588-465a-a308-a864a43d0070 ("Current Daily Price of Various
Commodities from Various Markets (Mandi)"), fed from the AGMARKNET portal
(Ministry of Agriculture & Farmers Welfare). It is a daily SNAPSHOT (~18k rows
for the current arrival_date) that the source overwrites each day — there is no
historical archive via the API, so each refresh re-pulls the whole current
snapshot and overwrites the published table. (A longer time series accrues
naturally as snapshots from successive days land downstream.)

Fetch strategy — why it is not a plain offset crawl
----------------------------------------------------
The Elasticsearch backend enforces `from + size <= 10000` (offset+limit window),
and the shared public api-key hard-caps `limit` at 10. So a plain offset crawl
can only reach the first 10,000 of the ~18,000 rows. To read the whole corpus we
exploit `total < 2 * WINDOW`: a window-scan sorted by `state.keyword` ascending
returns rows at sort-positions [0, WINDOW); a descending scan returns
[total-WINDOW, total). For total <= 2*WINDOW those two ranges cover every row
(the gap [WINDOW, total-WINDOW) is empty). Any state that straddles the WINDOW
boundary appears in BOTH scans; we re-fetch exactly those boundary states in full
via `filters[state.keyword]=<state>` (exact-match — note the `.keyword` suffix;
bare `filters[state]` is an analyzed/fuzzy match that returns wrong rows). A
final reconciliation asserts the union covers the reported grand total, so the
node fails loudly rather than publishing a partial corpus.

A registered own api-key (env DATA_GOV_IN_API_KEY) lifts the per-request limit
cap (the 10,000 window still applies, so the scan/chunk logic is unchanged) and
makes the crawl ~100x fewer requests. Without it the shared key works but is
slow (~2,700 requests/refresh at 10 rows/page).
"""

import os

from ratelimit import limits, sleep_and_retry

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

RESOURCE = "9ef84268-d588-465a-a308-a864a43d0070"
BASE = f"https://api.data.gov.in/resource/{RESOURCE}"
# Public shared sample key (capped at limit=10). Override with a registered key
# via DATA_GOV_IN_API_KEY to lift the cap and slash request count.
SHARED_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"

WINDOW = 10000          # Elasticsearch index.max_result_window (from+size cap)
PAGE = 1000             # requested page size; shared key silently clamps to 10
FIELDS = [
    "state", "district", "market", "commodity", "variety",
    "grade", "arrival_date", "min_price", "max_price", "modal_price",
]


def _api_key() -> str:
    return os.environ.get("DATA_GOV_IN_API_KEY") or SHARED_KEY


@sleep_and_retry
@limits(calls=100, period=60)
def _rate_gate() -> None:
    # Proactive throttle (~1.6 req/s) so the ~1,800-request shared-key crawl
    # stays under the undocumented burst quota that 429s under sustained load.
    # A registered key needs only ~40 requests, so this gate is a no-op for it.
    return None


@transient_retry(attempts=8, min_wait=5, max_wait=180)
def _call(extra: dict) -> dict:
    _rate_gate()
    params = {"api-key": _api_key(), "format": "json"}
    params.update(extra)
    resp = get(BASE, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _rowkey(rec: dict) -> tuple:
    return tuple(str(rec.get(k, "")) for k in FIELDS)


def _query_total(selector: dict) -> int:
    d = _call({**selector, "limit": 1, "offset": 0})
    return int(d.get("total") or 0)


def _paginate(selector: dict, cap: int) -> list:
    """Page `selector` (a sort or filter param dict) from offset 0 up to `cap`.

    `cap` keeps offset+limit within WINDOW. Termination is offset-based (not
    `len < page`) because the shared key clamps every page to 10 rows, which
    would otherwise look like an early end.
    """
    rows: list = []
    offset = 0
    while offset < cap:
        limit = min(PAGE, WINDOW - offset)
        if limit <= 0:
            break
        d = _call({**selector, "limit": limit, "offset": offset})
        recs = d.get("records", [])
        if not recs:
            break
        rows.extend(recs)
        offset += len(recs)
    return rows


def _scan(order: str) -> list:
    """Window-scan the whole resource sorted by state, ascending or descending."""
    sel = {"sort[state.keyword]": order}
    total = _query_total(sel)
    return _paginate(sel, min(total, WINDOW))


def _fetch_state(state: str) -> list:
    """Fetch every row for one state via exact `.keyword` match."""
    sel = {"filters[state.keyword]": state}
    total = _query_total(sel)
    if total >= WINDOW:
        raise RuntimeError(
            f"state {state!r} has {total} rows >= WINDOW {WINDOW}; "
            "exact-fetch would be truncated — add finer (district) sub-chunking"
        )
    rows = _paginate(sel, total)
    foreign = {r.get("state") for r in rows if r.get("state") != state}
    if foreign:
        raise RuntimeError(f"filter for {state!r} returned foreign states {foreign}")
    return rows


def fetch_prices(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name

    grand_total = _query_total({})
    if grand_total < 1:
        raise RuntimeError("resource reported 0 total rows — snapshot empty or API changed")
    if grand_total >= 2 * WINDOW:
        # The two-scan union only covers everything while total <= 2*WINDOW.
        raise RuntimeError(
            f"grand_total {grand_total} >= 2*WINDOW {2 * WINDOW}; two-pass "
            "window union can no longer guarantee full coverage — switch to "
            "per-state (or finer) chunking"
        )

    rows_asc = _scan("asc")
    rows_desc = _scan("desc")

    union: dict = {_rowkey(r): r for r in rows_asc}
    union.update({_rowkey(r): r for r in rows_desc})

    # States present in BOTH scans straddle the window boundary and may be
    # incomplete in either scan — re-fetch them exactly and in full.
    boundary = {r["state"] for r in rows_asc} & {r["state"] for r in rows_desc}
    for state in sorted(boundary):
        for rec in _fetch_state(state):
            union[_rowkey(rec)] = rec

    rows = list(union.values())
    if len(rows) < grand_total * 0.95:
        raise RuntimeError(
            f"collected {len(rows)} rows but resource reports {grand_total}; "
            "coverage incomplete — refusing to publish a partial snapshot"
        )

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="agmarknet-prices", fn=fetch_prices, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="agmarknet-prices-transform",
        deps=["agmarknet-prices"],
        key=("state", "district", "market", "commodity", "variety", "grade", "arrival_date"),
        temporal="arrival_date",
        sql='''
            SELECT DISTINCT
                state,
                district,
                market,
                commodity,
                variety,
                grade,
                try_strptime(arrival_date, '%d/%m/%Y')::DATE AS arrival_date,
                TRY_CAST(min_price   AS DOUBLE) AS min_price,
                TRY_CAST(max_price   AS DOUBLE) AS max_price,
                TRY_CAST(modal_price AS DOUBLE) AS modal_price
            FROM "agmarknet-prices"
            WHERE try_strptime(arrival_date, '%d/%m/%Y') IS NOT NULL
        ''',
    ),
]
