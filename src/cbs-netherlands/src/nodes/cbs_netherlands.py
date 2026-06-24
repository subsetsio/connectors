"""CBS (Netherlands) — StatLine open data connector.

Source: Statistics Netherlands (CBS) StatLine, exposed as OData v3.

Access strategy (per research): the catalog at
``https://opendata.cbs.nl/ODataCatalog/Tables`` enumerates every StatLine
table; each table's data is fetched per-table from the OData **Feed**
(``https://opendata.cbs.nl/ODataFeed/odata/{id}/TypedDataSet``). The Feed has
no per-call cell cap (unlike the standard ODataApi) but it does apply
server-driven paging at 10000 rows via an ``odata.nextLink``, which we follow
to completion.

Fetch shape — **stateless full re-pull** (implement-prompt shape 1). CBS tables
are revised in place (provisional → revised → definite), so we never trust a
stored row-level high-water mark: each refresh re-snapshots the whole table
from ``$skip=0`` and overwrites the single raw asset. The TypedDataSet endpoint
exposes no row-level ``since``/``modifiedAfter`` filter, so genuine incremental
is not possible here; the only delta signal is table-level ``Modified`` on the
catalog, which the (later) maintain step uses to decide whether a table needs
re-fetching at all. A handful of tables are very large (tens of millions of
rows → thousands of pages); the full crawl is therefore expensive, which is the
documented cost of having no row-level delta filter. Memory stays bounded by
streaming each row straight to a gzipped NDJSON file rather than buffering.

Raw format — **NDJSON**. Every table has its own column set (each StatLine
table is a distinct dimension/topic schema), so a single shared parquet schema
is impossible; NDJSON re-types per table on read. One raw asset per table
(exact-name view), so the transform is a thin pass-through publish.
"""

import json
import socket


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_writer,
    transient_retry,
)

# ---------------------------------------------------------------------------
# Source surface
# ---------------------------------------------------------------------------

FEED_BASE = "https://opendata.cbs.nl/ODataFeed/odata"
PAGE_SIZE = 10000          # server-driven page size observed on the Feed
MAX_PAGES = 200_000        # safety ceiling (~2e9 rows); raises, never silent

# The rank-accepted entity union — original-case StatLine table identifiers.
# Inlined per the catalog-connector contract (no module-level I/O).
from constants import ENTITY_IDS


def _node_id(entity_id: str) -> str:
    """Map a StatLine identifier to its download spec id (and asset name)."""
    return f"cbs-netherlands-{entity_id.lower().replace('_', '-')}"


# Reverse lookup: spec id -> original-case identifier (needed because the
# transform back from a lowercased/dash-normalised id is ambiguous, e.g.
# '7052_95'). Pure in-memory derivation, no I/O.
_EID_BY_NODE = {_node_id(eid): eid for eid in ENTITY_IDS}


# ---------------------------------------------------------------------------
# HTTP with honest retry semantics
# ---------------------------------------------------------------------------


# opendata.cbs.nl publishes both A and AAAA records, but the cloud runners have
# no IPv6 egress — connecting to the AAAA address raises ENETUNREACH ([Errno 101]
# Network is unreachable) and never falls back to IPv4. Force IPv4 resolution
# process-wide (each spec runs in its own subprocess; everything it talks to —
# CBS and R2 — is reachable over IPv4).
_orig_getaddrinfo = socket.getaddrinfo
_ipv4_forced = False


def _force_ipv4() -> None:
    global _ipv4_forced
    if _ipv4_forced:
        return

    def _ipv4_only(host, port, family=0, type=0, proto=0, flags=0):
        return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)

    socket.getaddrinfo = _ipv4_only
    _ipv4_forced = True


# A full-corpus crawl runs for hours and hammers one host; opendata.cbs.nl
# answers deep `$skip` pages but intermittently throws a transient 503 under
# sustained load (observed mid-crawl on a large table). The standard 6-attempt
# policy exhausted inside one bad window and crashed the whole DAG, so widen the
# budget: 10 attempts with backoff to 300s rides out a multi-minute server
# wobble without giving up. 429/5xx/network errors are all `is_transient`.
@transient_retry(attempts=10, min_wait=4, max_wait=300)
def _fetch_page(url: str, params: dict | None = None) -> dict:
    resp = get(url, params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Download — one stateless full snapshot per StatLine table
# ---------------------------------------------------------------------------

def fetch_one(node_id: str) -> None:
    """Stream a StatLine table's full TypedDataSet to one gzipped NDJSON asset.

    Stateless: re-fetches from the first page every run and overwrites, so
    in-place revisions are always picked up. Follows ``odata.nextLink`` until
    the Feed stops paging.
    """
    _force_ipv4()
    asset = node_id
    entity_id = _EID_BY_NODE[node_id]

    url = f"{FEED_BASE}/{entity_id}/TypedDataSet"
    params = {"$format": "json"}

    pages = 0
    rows_written = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as fh:
        while url is not None:
            if pages >= MAX_PAGES:
                raise RuntimeError(
                    f"{asset}: exceeded MAX_PAGES={MAX_PAGES} (source grew "
                    f"past expectations) — investigate before raising the cap"
                )
            payload = _fetch_page(url, params)
            params = None  # nextLink already carries $skip/$format
            for row in payload.get("value", []):
                fh.write(json.dumps(row, ensure_ascii=False))
                fh.write("\n")
                rows_written += 1
            pages += 1
            url = payload.get("odata.nextLink") or payload.get("@odata.nextLink")

    print(f"  {asset}: wrote {rows_written} rows across {pages} page(s)")


DOWNLOAD_SPECS = [
    NodeSpec(id=_node_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# ---------------------------------------------------------------------------
# Transform — one published Delta table per StatLine table
# ---------------------------------------------------------------------------
# Each table has its own dimension/topic schema, so the transform is a thin
# typed pass-through: drop the internal OData row index ``ID`` (a meaningless
# sequential counter) and publish the rest as-is. DuckDB's read_json_auto
# infers each table's per-column types from the NDJSON; a 0-row result fails
# the node, which is the correctness gate on the raw fetch.

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * EXCLUDE (ID) FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
