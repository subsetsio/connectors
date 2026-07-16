"""EPA Envirofacts connector.

Pulls the full contents of EPA Envirofacts relational tables/views via the
Envirofacts Data Service API V1 (https://data.epa.gov/dmapservice/). Each
accepted collect entity is one `[program].[table]` target pulled in full.

Access shape: stateless full re-pull (download prompt shape 1). Envirofacts
exposes NO incremental query surface -- no since/modifiedAfter/cursor parameter
on the dmapservice tables, and no count endpoint -- so every refresh re-pulls
each table in full. The cost of that is documented here rather than papered
over with a watermark the API cannot support.

Wire format vs raw format
-------------------------
Windows are requested as PARQUET and stored as gzip-NDJSON fragments.

PARQUET on the wire because it is ~1000x cheaper than JSON: measured
tri.tri_release_qty/1:200000 = 200k rows in 457KB. The API serves a whole
[first:last] window in ONE request, so a table is tens of requests, not
thousands.

NDJSON on disk because the API infers column types PER WINDOW: a column whose
values are all NULL within a window comes back typed `null` (measured:
tri.tri_chem_info.csc_ind, tri.tri_release_qty.non_prod_release). A column that
is all-null in an early window and populated in a later one therefore changes
parquet type mid-table, and the per-window parquet files would not glob-union
at read time. NDJSON carries no schema contract; the transform re-types on
read, and the 401 live tables span 13 program systems whose schemas we do not
control.

Pagination, and how slow it really is
-------------------------------------
The row-window segment is 1-indexed and inclusive: `t/1:1000` returns rows
1..1000. There is no keyset alternative: of the documented column operators
only `equals` parses (`>`, `<`, `greater_than` all return a parse error), and
even an equality probe on the primary key of icis.icis_dmr_form_value took 88s
-- the backend scans, it does not seek.

Throughput is bounded per ROW, not per offset. Measured on
icis.icis_dmr_form_value, 1M-row PARQUET windows: 96s at offset 0, 91s at 25M,
147s at 50M, 140s at 100M -- roughly 7-11k rows/s and flat in depth, so a deep
window costs no more than a shallow one. That does not hold for every wide
FRS/ICIS view: 1M-row windows later returned HTTP 400 or disconnected after
long server-side work. PAGE_SIZE is therefore chosen for reliability, not
request-count minimization: 100k rows keeps slow wide views at roughly
40-65s/request while still preserving monotonic continuation.

The consequence is that this corpus is simply large: ~750M rows across 401
live tables at ~8k rows/s is on the order of 25 hours of fetching, and
icis.icis_dmr_form_value alone (100-200M rows) is ~5 hours. It cannot be
pulled in one 5.75h leg -- hence the continuation contract below.

Windows past the end of a table return HTTP 200 with a valid but EMPTY parquet
body (0 rows, 0 columns) -- that, and only that, terminates the loop. A short
window is NOT treated as the end: the API fills windows, and trusting a short
read would silently truncate a large table if the server ever returned a
partial page.

Continuation, and why this fn returns True
------------------------------------------
The cloud DAG runs sequentially (DAG_PARALLELISM defaults to 1) under a 5.75h
budget (DAG_TIME_BUDGET=20700). When that budget expires the supervisor kills
the in-flight node and resets it to `pending` -- and a killed node's staged raw
fragments are NEVER committed to the raw manifest, so every window it fetched
that leg is discarded. Only a node that RETURNS commits.

A table that needs more than one leg to drain would therefore restart from row
1 forever. So a fetch fn that runs out of its slice of the budget commits what
it has and returns True, which is the orchestrator's documented `pagination`
handshake: the node is marked done, its fragments commit, the run finalizes as
`needs_continuation`, and the next link is dispatched under the SAME run_id.
On that link the already-committed windows are skipped and the table resumes
where it left off. Progress is monotonic and every leg advances by at least one
window per node.

The slice is a fraction of DAG_TIME_BUDGET rather than the true remaining run
time because a forked child cannot see when the RUN started, only when it
itself started (see `hardened feedback epa --area subsets_utils`).

Fragments committed under a PRIOR run_id are last refresh's data, not this
one's: they are re-fetched, because this is a full re-pull and not an append.

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
import psutil
import pyarrow.parquet as pq

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, list_raw_fragments, load_state, raw_writer, save_state

BASE = "https://data.epa.gov/dmapservice/"

# Raw asset extension for every table. Kept in one place: the fragment manifest
# lookup and the writer must agree, or resume silently re-fetches everything.
EXT = "ndjson.gz"

# Rows per API request. 1M worked for some narrow tables but failed on wide
# FRS/ICIS views; 100k is the measured reliable size for those slower tables.
PAGE_SIZE = 100_000

# Rows converted from arrow to NDJSON at a time. Bounds peak RSS: a window is
# never materialised as one large list of Python dicts.
CHUNK_ROWS = 50_000

# Safety ceiling: 50k windows = 5 billion rows at PAGE_SIZE=100k, far past any
# Envirofacts table. Hitting it means the terminator never fired -- RAISE,
# never silently return a truncated table.
MAX_PAGES = 50_000

# State contract version. Bump when the resume/skip state shape changes.
STATE_VERSION = 1

# How long a permanent-404 table stays skipped before we probe it again.
SKIP_TTL_SECONDS = 14 * 86_400

# Fraction of the run's time budget one node may spend before it commits its
# fragments and asks for a continuation link. Sized so a leg fits ~3 saturated
# nodes: the node the deadline eventually kills loses at most this much work,
# and every node is guaranteed a turn within a few legs.
LEG_FRACTION = 0.30

# Fallback when DAG_TIME_BUDGET is unset (local dev): the cloud value.
DEFAULT_TIME_BUDGET_S = 20_700.0

# Do not start another Envirofacts window unless this much time remains before
# the parent DAG deadline. A single wide-table request can run for minutes, and
# colliding with the parent watchdog loses the node result even after raw writes.
WINDOW_DEADLINE_MARGIN_S = 45 * 60

# Set by src/main.py before load_nodes(). Forked children can see this, unlike
# the orchestrator's monotonic deadline, so long pulls can stop before the
# parent watchdog interrupts them.
RUN_STARTED_AT_ENV = "EPA_RUN_STARTED_AT"


def _leg_seconds() -> float:
    """Wall-clock this node may spend before committing and continuing."""
    try:
        budget = float(os.environ.get("DAG_TIME_BUDGET", "")) or DEFAULT_TIME_BUDGET_S
    except ValueError:
        budget = DEFAULT_TIME_BUDGET_S
    nominal = budget * LEG_FRACTION
    try:
        run_started = float(os.environ.get(RUN_STARTED_AT_ENV, ""))
    except ValueError:
        run_started = 0.0
    if run_started > 0:
        remaining = budget - max(0.0, time.time() - run_started) - WINDOW_DEADLINE_MARGIN_S
        return max(0.0, min(nominal, remaining))
    try:
        parent_started = psutil.Process(os.getppid()).create_time()
    except Exception:
        return nominal
    remaining = budget - max(0.0, time.time() - parent_started) - WINDOW_DEADLINE_MARGIN_S
    return max(0.0, min(nominal, remaining))


def _table_for(node_id: str) -> str:
    """Recover the Envirofacts `program.table` path from a spec/asset id.

    The id is `epa-{entity.lower().replace('_', '-')}`; the program separator is
    a dot (preserved) and underscores became dashes. Envirofacts table names
    contain no real dashes, so dash->underscore round-trips exactly.
    """
    return node_id[len("epa-") :].replace("-", "_")


def _fragment_for(page: int) -> tuple[int, int, str]:
    """The inclusive row-window and the fragment key for a zero-based page."""
    first = page * PAGE_SIZE + 1
    last = (page + 1) * PAGE_SIZE
    return first, last, f"{first:010d}-{last:010d}"


def _fetch_window(table: str, first: int, last: int):
    """Fetch one inclusive row-window [first:last] as an arrow Table.

    Transient errors (429/5xx/network) are retried by subsets_utils.get. A 4xx
    is permanent and propagates as httpx.HTTPStatusError for the caller to
    classify. The read timeout matches the server's 15-minute completion window.
    """
    url = f"{BASE}{table}/{first}:{last}/PARQUET"
    resp = get(url, timeout=(10.0, 900.0))
    resp.raise_for_status()
    if not resp.content:
        raise RuntimeError(f"{url}: HTTP 200 with an empty body (expected parquet)")
    return pq.read_table(io.BytesIO(resp.content))


def _write_fragment(asset: str, fragment: str, window) -> None:
    """Commit one row-window as a gzip-NDJSON raw fragment of `asset`.

    `default=str` renders types the JSON encoder does not carry natively
    (dates, decimals) rather than failing a whole window on one cell.
    """
    with raw_writer(asset, EXT, mode="wt", compression="gzip", fragment=fragment) as fh:
        for batch in window.to_batches(max_chunksize=CHUNK_ROWS):
            for row in batch.to_pylist():
                fh.write(json.dumps(row, separators=(",", ":"), default=str))
                fh.write("\n")


def _load_run_state(asset: str, run_id: str) -> dict:
    """This asset's state, but only the parts written by the CURRENT run.

    A prior run's state describes a prior refresh: its window count says nothing
    about the pull now in progress, so it is ignored rather than trusted.
    """
    state = load_state(asset)
    if state.get("schema_version") != STATE_VERSION:
        return {}
    if state.get("run_id") != run_id:
        return {}
    return state


def _skipped(asset: str) -> dict | None:
    """A live (unexpired) skipped marker for this asset, else None."""
    state = load_state(asset)
    if state.get("schema_version") != STATE_VERSION:
        return None
    skip = state.get("skipped")
    if skip and skip.get("expires_at", 0) > time.time():
        return skip
    return None


def fetch_one(node_id: str) -> bool | None:
    """Pull one Envirofacts table in full, one committed fragment per window.

    Returns True when the table is not yet drained and this leg's slice of the
    time budget is spent -- the orchestrator reads that as `needs_continuation`,
    commits this node's fragments, and dispatches the next link under the same
    run_id. Returns None when the table is fully drained.

    The runtime passes the spec id, which is also the asset name. Freshness
    gating is the maintain step's job -- if this is invoked, we fetch.
    """
    asset = node_id
    table = _table_for(node_id)

    skip = _skipped(asset)
    if skip is not None:
        print(f"  -> {table}: skipped ({skip['reason']}); re-probed once the marker expires")
        return None

    run_id = os.environ.get("RUN_ID", "unknown")
    state = _load_run_state(asset, run_id)

    # The raw manifest is the ONLY trustworthy done-set: an object it does not
    # reference does not exist, and a killed leg's writes are unreferenced.
    committed = {
        frag
        for frag, meta in list_raw_fragments(asset, EXT).items()
        if meta.get("run_id") == run_id
    }

    # Fast path: this run already drained the table. `total_windows` is only
    # trusted when the manifest still shows every one of those windows, so a
    # discarded leg re-opens the pull instead of silently declaring it done.
    total_windows = state.get("total_windows")
    if isinstance(total_windows, int) and len(committed) >= total_windows > 0:
        print(f"  -> {table}: already drained this run ({total_windows} windows)")
        return None

    deadline = time.monotonic() + _leg_seconds()
    fetched = 0

    for page in range(MAX_PAGES):
        first, last, fragment = _fragment_for(page)

        if fragment in committed:
            continue

        # Checked only before a window we would actually fetch. If the parent
        # DAG is inside the safety margin, return the continuation handshake
        # instead of starting a request that the watchdog will kill before the
        # child result is collected.
        if time.monotonic() >= deadline:
            print(
                f"  -> {table}: leg budget spent at window {page} "
                f"({fetched:,} rows this leg); committing and continuing next link"
            )
            return True

        try:
            window = _fetch_window(table, first, last)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404 and page == 0:
                # The table is gone upstream, not a transport failure. Record it
                # and return cleanly: one retired table must not fail the run.
                print(f"  -> {table}: HTTP 404, table retired upstream - skipping")
                save_state(
                    asset,
                    {
                        "schema_version": STATE_VERSION,
                        "run_id": run_id,
                        "skipped": {
                            "table": table,
                            "reason": "upstream returns HTTP 404 (table not found)",
                            "expires_at": int(time.time()) + SKIP_TTL_SECONDS,
                        },
                    },
                )
                return None
            raise

        # A window past the end of the table is the ONLY end-of-table signal.
        if window.num_rows == 0 and page > 0:
            _finish(asset, run_id, page)
            break

        # Raw first, state after: a crash between them re-fetches a window; the
        # reverse would record a window that was never committed.
        _write_fragment(asset, fragment, window)
        fetched += window.num_rows

        # An empty page 0 means the table itself is empty. The fragment above is
        # its honest 0-row snapshot; the asset exists.
        if window.num_rows == 0:
            _finish(asset, run_id, 1)
            break

        if time.monotonic() >= deadline:
            print(
                f"  -> {table}: leg budget spent after window {page} "
                f"({fetched:,} rows this leg); committing and continuing next link"
            )
            return True
    else:
        raise RuntimeError(
            f"{table}: hit MAX_PAGES={MAX_PAGES} ({fetched:,} rows fetched this leg) "
            "without reaching an empty window - investigate before raising the cap"
        )

    print(f"  -> {table}: drained, {fetched:,} rows fetched this leg")
    return None


def _finish(asset: str, run_id: str, total_windows: int) -> None:
    """Record how many windows constitute this table, for this run.

    Not a completion flag: it is scoped to `run_id`, and the fast path that
    reads it re-checks the manifest, so it can only ever skip work this run
    genuinely committed.
    """
    save_state(
        asset,
        {
            "schema_version": STATE_VERSION,
            "run_id": run_id,
            "total_windows": total_windows,
        },
    )


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"epa-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
