"""EPA Envirofacts connector.

Pulls the full contents of EPA Envirofacts relational tables/views via the
Envirofacts Data Service API V1 (https://data.epa.gov/dmapservice/). Each
accepted collect entity is one `[program].[table]` target pulled in full.

Access shape: stateless full re-pull (download prompt shape 1). Envirofacts
exposes NO incremental query surface -- no since/modifiedAfter/cursor parameter
on the dmapservice tables, and no count endpoint -- so every refresh re-pulls
each table in full and overwrites. The cost of that is documented here rather
than worked around with a watermark the API cannot support.

Wire format vs raw format
-------------------------
Windows are requested as PARQUET and stored as gzip-NDJSON fragments.

PARQUET on the wire because it is ~1000x cheaper than JSON: measured
tri.tri_release_qty/1:200000 = 200k rows in 457KB, versus tens of MB of JSON.
The API returns a whole [first:last] window in ONE request, so even the largest
table in the catalog (~60M rows) is ~60 requests rather than thousands.

NDJSON on disk because the API infers column types PER WINDOW: a column whose
values are all NULL within a window comes back typed `null` (measured:
tri.tri_chem_info.csc_ind, tri.tri_release_qty.non_prod_release). A column that
is all-null in an early window and populated in a later one would therefore
change parquet type mid-table, and the per-window parquet files would not
glob-union at read time. NDJSON carries no schema contract; the transform
re-types on read, and the 401 live tables span 13 program systems whose schemas
we do not control.

Pagination and resume
---------------------
The row-window segment is 1-indexed and inclusive: `t/1:1000` returns rows
1..1000. Windows past the end of a table return HTTP 200 with a valid but
EMPTY parquet body (0 rows, 0 columns) -- that, and only that, terminates the
loop. A short window is NOT treated as the end: the API fills windows, and
trusting a short read would silently truncate a large table if the server ever
returned a partial page.

Each window is committed as its own raw fragment, so a run that the supervisor
interrupts near its CI budget resumes from the last committed window instead of
restarting the table from row 1. Fragments carrying the CURRENT run_id are
already-done work for this refresh; fragments from an older run_id are last
refresh's data and are re-fetched (this is a full re-pull, not an append).

Dead and empty tables
---------------------
Probed 2026-07 against the live API: of the 416 accepted entities, 401 return
rows, 14 are genuinely empty (0 rows at any window -- e.g. tri.tri_county,
acres.congressional_district_assoc), and acres.ref_contact_type_old returns a
permanent HTTP 404 ("The table ... was not found"). An empty table still writes
one empty fragment, so the asset exists and records an honest 0-row snapshot.
A permanent 404 writes a TTL-bound skipped marker and returns cleanly, so one
retired table cannot fail the run; the marker expires so upstream recovery is
picked up without a human.
"""

from __future__ import annotations

import io
import json
import os
import time

import httpx
import pyarrow.parquet as pq

from constants import ENTITY_IDS
from subsets_utils import (
    NodeSpec,
    get,
    list_raw_fragments,
    load_state,
    raw_writer,
    save_state,
    transient_retry,
)

BASE = "https://data.epa.gov/dmapservice/"

# Raw asset extension for every table. Kept in one place: the fragment manifest
# lookup and the writer must agree or resume silently re-fetches everything.
EXT = "ndjson.gz"

# Rows per API request. The API serves a whole window in one request, and
# deep offsets get slower (measured: 1M rows of icis.icis_dmr_form_value took
# 33s at offset 1 and 134s at offset 40M), so the request count -- not the
# window size -- is what we minimise. 1M rows lands at ~3-11MB of parquet.
PAGE_SIZE = 1_000_000

# Rows converted from arrow to NDJSON at a time. Bounds peak RSS: a 1M-row
# window is never materialised as 1M python dicts at once.
CHUNK_ROWS = 50_000

# Safety ceiling: 5000 windows = 5 billion rows, far past any Envirofacts
# table. Hitting it means the terminator never fired -- RAISE, never silently
# return a truncated table.
MAX_PAGES = 5_000

# State contract version. Bump when the skipped-marker shape changes.
STATE_VERSION = 1

# How long a permanent-404 table stays skipped before we probe it again.
SKIP_TTL_SECONDS = 14 * 86_400


def _table_for(node_id: str) -> str:
    """Recover the Envirofacts `program.table` path from a spec/asset id.

    The id is `epa-{entity.lower().replace('_', '-')}`; the program separator is
    a dot (preserved) and underscores became dashes. Envirofacts table names
    contain no real dashes, so dash->underscore round-trips exactly.
    """
    return node_id[len("epa-") :].replace("-", "_")


@transient_retry()
def _fetch_window(table: str, first: int, last: int):
    """Fetch one inclusive row-window [first:last] as an arrow Table.

    Transient errors (429/5xx/network) are retried by the decorator. A 4xx is
    permanent and propagates as httpx.HTTPStatusError for the caller to
    classify. The 15-minute server-side completion window sets the read timeout.
    """
    url = f"{BASE}{table}/{first}:{last}/PARQUET"
    resp = get(url, timeout=(10.0, 900.0))
    resp.raise_for_status()
    if not resp.content:
        raise RuntimeError(f"{url}: HTTP 200 with an empty body (expected parquet)")
    return pq.read_table(io.BytesIO(resp.content))


def _write_fragment(asset: str, fragment: str, arrow_table) -> None:
    """Commit one row-window as a gzip-NDJSON raw fragment of `asset`.

    `default=str` renders types the JSON encoder does not carry natively
    (dates, decimals) rather than failing the whole window on one cell.
    """
    with raw_writer(asset, EXT, mode="wt", compression="gzip", fragment=fragment) as fh:
        for batch in arrow_table.to_batches(max_chunksize=CHUNK_ROWS):
            for row in batch.to_pylist():
                fh.write(json.dumps(row, separators=(",", ":"), default=str))
                fh.write("\n")


def _mark_skipped(asset: str, table: str, reason: str) -> None:
    save_state(
        asset,
        {
            "schema_version": STATE_VERSION,
            "skipped": {
                "table": table,
                "reason": reason,
                "expires_at": int(time.time()) + SKIP_TTL_SECONDS,
            },
        },
    )


def _active_skip(asset: str) -> dict | None:
    """The live skipped marker for this asset, or None (absent/expired/stale)."""
    state = load_state(asset)
    if state.get("schema_version") != STATE_VERSION:
        return None
    skip = state.get("skipped")
    if skip and skip.get("expires_at", 0) > time.time():
        return skip
    return None


def fetch_one(node_id: str) -> None:
    """Pull one Envirofacts table in full, one committed fragment per window.

    The runtime passes the spec id, which is also the asset name. Freshness
    gating is the maintain step's job -- if this is invoked, we fetch.
    """
    asset = node_id
    table = _table_for(node_id)

    skip = _active_skip(asset)
    if skip is not None:
        print(f"  -> {table}: skipped ({skip['reason']}); re-probed after TTL")
        return

    run_id = os.environ.get("RUN_ID", "unknown")
    done = {
        frag
        for frag, meta in list_raw_fragments(asset, EXT).items()
        if meta.get("run_id") == run_id
    }
    fetched = 0

    for page in range(MAX_PAGES):
        first = page * PAGE_SIZE + 1
        last = (page + 1) * PAGE_SIZE
        fragment = f"{first:010d}-{last:010d}"

        if fragment in done:
            continue

        try:
            window = _fetch_window(table, first, last)
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            if status == 404 and page == 0:
                # The table is gone upstream, not a transport failure. Record it
                # and return cleanly: one retired table must not fail the run.
                print(f"  -> {table}: HTTP 404, table retired upstream - skipping")
                _mark_skipped(asset, table, "upstream returns HTTP 404 (table not found)")
                return
            raise

        # A window past the end of the table is the ONLY end-of-table signal.
        # On page 0 an empty window means the table itself is empty: still commit
        # the fragment, so the asset exists as an honest 0-row snapshot.
        if window.num_rows == 0 and page > 0:
            break

        _write_fragment(asset, fragment, window)
        fetched += window.num_rows

        if window.num_rows == 0:
            break
    else:
        raise RuntimeError(
            f"{table}: hit MAX_PAGES={MAX_PAGES} ({fetched:,} rows fetched this leg) "
            "without reaching an empty window - investigate before raising the cap"
        )

    print(f"  -> {table}: {fetched:,} rows fetched this leg ({len(done)} windows already done)")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"epa-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
