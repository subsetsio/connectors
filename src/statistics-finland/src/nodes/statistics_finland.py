"""Statistics Finland (StatFin) — PxWeb v1 catalog connector.

One download node per StatFin table (the rank-accepted entity union, listed in
``constants.ENTITY_PATHS``). Each node:

  1. GETs the table's PxWeb metadata (dimensions + value codes),
  2. POSTs json-stat2 queries selecting every value of every dimension, chunked
     so no single request exceeds the per-query cell cap (split adaptively if the
     server still rejects a chunk as too large), and
  3. expands each json-stat2 hypercube into tidy long-format rows — one row per
     non-null cell, one column per dimension (English label), plus numeric
     ``value``.

The matching transform publishes that tidy table 1:1.

Operational notes (learned from the source):
  * The DAG runs sequentially, so a fixed pause before every HTTP call is a true
    global throttle. PxWeb caps ~30 queries / 10s AND ~40 / 60s sustained, 429ing
    over either — pacing under the sustained cap avoids backoff storms entirely.
  * The documented 100k-cell cap is optimistic; some tables 400/403 well below
    it. We target a conservative chunk size and split any chunk the server still
    refuses, so we adapt to each table's real limit without guessing.
  * A full pull of all ~1535 tables costs ~15h of paced HTTP — far more than one
    GitHub job's ~5h45m budget, so a run ALWAYS spans several continuation legs.
    The orchestrator does not carry node status across legs (every leg starts
    every spec `pending`), so without a maintain check each leg re-downloads the
    same leading prefix of tables and the chain never converges — exactly the
    2026-07-02 runaway (31 legs, ~7.5 days of CI, 578/1535 done every leg).
    ``MAINTAIN_SPECS`` below is what makes the backfill resumable: a table whose
    raw was committed inside the refresh window is skipped before its subprocess
    spawns, so each leg advances into new tables and the run terminates.
"""

import re
import time

import httpx
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    post,
    raw_asset_exists,
    save_raw_ndjson,
    transient_retry,
)
from subsets_utils.retry import is_transient
from constants import ENTITY_PATHS

_BASE = "https://pxdata.stat.fi/PXWeb/api/v1/en"
_PREFIX = "statistics-finland-"
_CELL_TARGET = 40000   # conservative chunk size (server 400s above ~40-80k on some tables)
_PACE_S = 1.3          # min seconds between HTTP calls — stay under ~40 req / 60s
_RAW_EXT = "ndjson.zst"

# Matches maintenance.json's cadence_days. PxWeb exposes no since/modifiedAfter
# parameter, so a refresh is a full re-pull: on a due run every table is older
# than the window and re-fetched, and each leg then skips what earlier legs of
# the SAME run just wrote — the window doubles as the resume marker.
MAINTAIN_MAX_AGE_DAYS = 7


def _throttle():
    time.sleep(_PACE_S)


def _meta_retryable(exc):
    """Retry predicate for the metadata GET. Same as the standard transient set
    (network errors / 429 / 5xx) PLUS client 400/403: PxWeb intermittently
    rejects the metadata endpoint with 400/403 under load even for valid tables
    (confirmed — a table that 400s here returns 200 on a later try). Without
    this, one transient blip raises out of fetch_one, fails the node, and flips
    the whole run's status from continuation to 'failed', suppressing the
    retrigger and stranding the other ~1000 tables (the 2026-06-22 failure)."""
    if is_transient(exc):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in (400, 403)
    return False


@retry(retry=retry_if_exception(_meta_retryable), stop=stop_after_attempt(8),
       wait=wait_exponential(min=4, max=90), reraise=True)
def _get_meta(url):
    _throttle()
    r = get(url, timeout=(10.0, 120.0))
    r.raise_for_status()
    return r.json()


@transient_retry(attempts=8, max_wait=90)
def _post_data(url, query):
    _throttle()
    r = post(url, json={"query": query, "response": {"format": "json-stat2"}},
             timeout=(10.0, 180.0))
    r.raise_for_status()
    return r.json()


def _to_query(sel):
    return [{"code": code, "selection": {"filter": "item", "values": vals}}
            for code, vals in sel.items()]


def _sanitize(text, used):
    """Turn a dimension label into a unique snake_case column name."""
    name = re.sub(r"[^0-9a-z]+", "_", text.strip().lower()).strip("_") or "dim"
    if name == "value":  # reserve `value` for the numeric measure
        name = "value_dim"
    base, i = name, 2
    while name in used:
        name = f"{base}_{i}"
        i += 1
    used.add(name)
    return name


def _chunks(dims, limit):
    """Yield query selections (code -> [value codes]) each <= ``limit`` cells.

    ``dims`` is a list of (code, values) sorted descending by cardinality, so the
    largest dimension is split first; very large tables recurse onto further dims.
    """
    total = 1
    for _, v in dims:
        total *= len(v)
    if total <= limit:
        yield {c: list(v) for c, v in dims}
        return
    code0, vals0 = dims[0]
    rest = dims[1:]
    rest_total = 1
    for _, v in rest:
        rest_total *= len(v)
    if rest_total <= limit:
        step = max(1, limit // rest_total)
        for i in range(0, len(vals0), step):
            sel = {code0: vals0[i:i + step]}
            for c, v in rest:
                sel[c] = list(v)
            yield sel
    else:
        for val in vals0:
            for sub in _chunks(rest, limit):
                out = {code0: [val]}
                out.update(sub)
                yield out


def _fetch_selection(url, sel):
    """POST one selection; if the server rejects it as too large (400/403), split
    along its largest dimension and recurse. Yields json-stat2 docs. A selection
    that cannot be split further and still fails is skipped (returns nothing)."""
    try:
        yield _post_data(url, _to_query(sel))
        return
    except httpx.HTTPStatusError as e:
        if e.response.status_code not in (400, 403):
            raise  # genuinely unexpected — let it surface
    code, vals = max(sel.items(), key=lambda kv: len(kv[1]))
    if len(vals) <= 1:
        print(f"[statfin] skipping unsplittable rejected block at {url}: {sel}")
        return
    mid = len(vals) // 2
    for half in (vals[:mid], vals[mid:]):
        sub = dict(sel)
        sub[code] = half
        yield from _fetch_selection(url, sub)


def _expand(doc, colmap):
    """Expand a json-stat2 dataset doc into tidy row dicts (null cells dropped)."""
    ids = doc["id"]
    sizes = doc["size"]
    values = doc["value"]
    dim = doc["dimension"]
    pos2code = {}
    code2label = {}
    for c in ids:
        cat = dim[c]["category"]
        idx = cat["index"]
        if isinstance(idx, dict):
            arr = [None] * len(idx)
            for code, p in idx.items():
                arr[p] = code
        else:
            arr = list(idx)
        pos2code[c] = arr
        code2label[c] = cat.get("label", {})
    for k in range(len(values)):
        v = values[k]
        if v is None:
            continue
        rem = k
        row = {}
        for i in range(len(ids) - 1, -1, -1):
            c = ids[i]
            p = rem % sizes[i]
            rem //= sizes[i]
            row[colmap[c]] = code2label[c].get(pos2code[c][p], pos2code[c][p])
        row["value"] = v
        yield row


def fetch_one(node_id):
    asset = node_id
    entity = node_id[len(_PREFIX):] if node_id.startswith(_PREFIX) else node_id
    url = f"{_BASE}/{ENTITY_PATHS[entity]}"

    meta = _get_meta(url)
    variables = meta["variables"]
    used = set()
    colmap = {v["code"]: _sanitize(v["text"], used) for v in variables}
    dims = sorted(((v["code"], v["values"]) for v in variables),
                  key=lambda cv: len(cv[1]), reverse=True)

    def rows():
        skipped = 0
        for sel in _chunks(dims, _CELL_TARGET):
            try:
                for doc in _fetch_selection(url, sel):
                    yield from _expand(doc, colmap)
            except Exception as e:  # one flaky chunk must not abort the whole run
                skipped += 1
                print(f"[statfin] {asset}: chunk failed ({type(e).__name__}: {e}); skipping")
        if skipped:
            print(f"[statfin] {asset}: {skipped} chunk(s) skipped after retries")

    save_raw_ndjson(rows(), asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"statistics-finland-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_PATHS
]


def _is_fresh(asset_id):
    """Skip a table whose raw was committed inside the refresh window.

    Resolved against the raw manifest, so it sees fragments written by earlier
    continuation legs of this same run — that is what lets the multi-leg
    backfill make forward progress instead of restarting at table 1.
    """
    return raw_asset_exists(asset_id, _RAW_EXT, max_age_days=MAINTAIN_MAX_AGE_DAYS)


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            f"Full re-pull when raw is older than {MAINTAIN_MAX_AGE_DAYS}d. PxWeb has no "
            "since/modifiedAfter parameter, so a refresh re-fetches the whole table; the "
            "window doubles as the resume marker across continuation legs. Statistics "
            "Finland publishes per-table release calendars at "
            "https://stat.fi/en/statistics-release-calendar"
        ),
        check=_is_fresh,
    )
    for spec in DOWNLOAD_SPECS
]
