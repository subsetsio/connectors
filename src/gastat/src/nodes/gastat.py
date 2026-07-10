"""GASTAT (Saudi General Authority for Statistics) — download + transform.

Mechanism: the GASTAT Open Data API (CData API Server, OData semantics) at
https://api.stats.gov.sa/v1/stats/{TABLE_CODE}. Public, no key. One endpoint
per published statistical table; each table has its own dimension set (its own
column list), so this is a catalog connector — one generic fetch over every
table code in the rank-accepted entity union.

We pull each table as CSV (CData emits a deterministic header+rows CSV for any
table regardless of its dimensions), page through it with $top/$skip offset
pagination, and persist line-delimited NDJSON (schemas differ table-to-table,
so a single declared parquet schema can't cover them — NDJSON re-types on read).
Each transform publishes one Delta table straight from its table's raw asset.
"""

import csv
import io
import os

from subsets_utils import NodeSpec, get, save_raw_ndjson, transient_retry

from constants import ENTITY_IDS

BASE = "https://api.stats.gov.sa/v1/stats"

# Page size for $top/$skip. The CData gateway grows slow per-request and starts
# returning 504s well before any row limit (the latency is fixed server-side
# overhead, not row volume — small tables 504 at top=10000 too); a 5k page keeps
# every request comfortably under the gateway timeout while still being one or
# two requests for the largest tables here.
PAGE = 5000

# Safety ceiling: a single GASTAT table exceeding 10M rows would be wildly
# beyond any observed table and signals runaway pagination — raise, don't loop.
MAX_PAGES_ABS = 1000

API_KEY_ENV = "GASTAT_API_KEY"


def _spec_id(code: str) -> str:
    return f"gastat-{code.lower().replace('_', '-')}"


def _api_headers() -> dict[str, str]:
    api_key = os.environ.get(API_KEY_ENV)
    if not api_key:
        raise RuntimeError(
            f"{API_KEY_ENV} is required: GASTAT now requires an 'apikey' "
            "request header for https://api.stats.gov.sa/v1/stats endpoints"
        )
    return {"apikey": api_key}


# spec id -> original table code (round-trips through the lower/hyphen id form;
# table codes are upper-case + underscores, so this map is the authoritative
# recovery path rather than re-uppercasing the id).
CODE_BY_SPEC = {_spec_id(code): code for code in ENTITY_IDS}


@transient_retry()
def _fetch_csv_page(code: str, skip: int, top: int) -> str:
    """One CSV page. 5xx (incl. the CData license 500) and 429 are retried by
    transient_retry, then reraised — a persistent upstream outage fails the
    node loudly rather than writing a partial/empty asset."""
    url = f"{BASE}/{code}"
    resp = get(
        url,
        params={"format": "CSV", "$top": top, "$skip": skip},
        headers=_api_headers(),
        timeout=180,
    )
    resp.raise_for_status()
    return resp.text


def fetch_one(node_id: str) -> None:
    code = CODE_BY_SPEC[node_id]

    rows: list[dict] = []
    skip = 0
    pages = 0
    while True:
        if pages >= MAX_PAGES_ABS:
            raise RuntimeError(
                f"{code}: hit {MAX_PAGES_ABS}-page safety ceiling "
                f"({pages * PAGE}+ rows) — pagination likely not terminating"
            )
        text = _fetch_csv_page(code, skip, PAGE)
        batch = list(csv.DictReader(io.StringIO(text)))
        rows.extend(batch)
        pages += 1
        if len(batch) < PAGE:
            break
        skip += PAGE

    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(code), fn=fetch_one, kind="download")
    for code in ENTITY_IDS
]
