"""Statistics Canada connector.

One published Delta table per accepted StatCan data cube (productId). Access is
the WDS bulk full-table CSV path (research mechanism `bulk_csv`): the
getFullTableDownloadCSV resolver returns a stable per-table zip URL; the zip
holds {productId}.csv (full history, all coordinates) plus a metadata CSV. We
stream the zip to a local scratch file (memory-bounded — never the whole zip in
RAM) then stream the inner data CSV straight to raw (the inner CSV can be 1GB+
uncompressed); a generic DuckDB transform types the VALUE column and publishes.

Fetch shape: stateless full re-pull. Each cube is small-to-large but fetchable
in one request; the bulk zip always carries the complete table, so there is no
watermark/cursor — every run overwrites with the current full table, picking up
revisions for free. No auth (open service). WDS documents 50 req/s server-wide,
25 req/s per IP; node specs run sequentially in separate processes, so the only
pacing we add is the per-table retry backoff below.

Resilience matters here more than in a small connector. The corpus is ~3.5k
tables — far more than one CI run's wall-clock budget — so a run drains a slice
and the runner self-retriggers a continuation until the whole catalog is done.
That continuation chain only survives while NO node ends in "failed": the DAG's
overall status is "failed" the moment any single node fails, which aborts the
chain (no retrigger). A deadline-interrupted in-flight node is reset to
"pending" (safe — it just resumes next run), but an *exception* marks the node
"failed". So every table fetch is wrapped in a long-horizon retry that outlasts
transient WDS hiccups (throttles, dropped connections, momentary 5xx, truncated
zips) rather than letting one flaky table kill the chain.
"""
import os
import tempfile
import zipfile

from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    get_client,
    is_transient,
    raw_writer,
)

SLUG = "statistics-canada"
_RESOLVE_URL = "https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/{pid}/en"
_CHUNK = 1 << 20  # 1 MiB
_CONNECT_TIMEOUT = 30.0
# Per-*chunk* read timeout: because we stream the body chunk-by-chunk it bounds a
# single stalled read, never the whole (1GB+) transfer — a steady-but-slow large
# download won't trip it, while a genuinely stalled socket raises a retryable
# ReadTimeout.
_READ_TIMEOUT = 300.0


class _RetryableSource(RuntimeError):
    """A source-side condition we expect to clear on retry — the resolver not yet
    returning SUCCESS (e.g. a momentary WDS maintenance window). Distinct from a
    code bug so the retry predicate can target it without being a catch-all."""


def _is_retryable(exc: BaseException) -> bool:
    """Broaden the standard transient classification with the two extra
    source-side failure modes this bulk path can hit: a not-yet-SUCCESS resolver
    response and a truncated/corrupt zip (a partial download surfaces as
    BadZipFile when we open it)."""
    return is_transient(exc) or isinstance(exc, (_RetryableSource, zipfile.BadZipFile))


# 9 attempts, exponential 10..300s ≈ up to ~20 min of cumulative waiting before
# giving up — long enough to outlast a WDS per-IP throttle or a flaky table,
# short enough that one genuinely-dead table can't consume a whole run's budget.
_table_retry = retry(
    retry=retry_if_exception(_is_retryable),
    stop=stop_after_attempt(9),
    wait=wait_exponential(min=10, max=300),
    reraise=True,
)


def _resolve_zip_url(pid: str) -> str:
    """Resolve a productId to its stable full-table CSV zip URL via WDS."""
    resp = get(_RESOLVE_URL.format(pid=pid), timeout=(_CONNECT_TIMEOUT, 120.0))
    resp.raise_for_status()  # 429/5xx -> is_transient -> retried by _table_retry
    payload = resp.json()
    rec = payload[0] if isinstance(payload, list) else payload
    if not isinstance(rec, dict):
        raise _RetryableSource(f"WDS resolve: unexpected payload for {pid}: {payload!r:.200}")
    if rec.get("status") != "SUCCESS" or not rec.get("object"):
        raise _RetryableSource(f"WDS resolve not SUCCESS for {pid}: status={rec.get('status')!r}")
    return rec["object"]


def _download_zip(url: str, dest_path: str) -> None:
    """Stream the full-table zip to a local scratch file (compressed, tens-to-
    hundreds of MB) rather than buffering it in RAM — a spawn-subprocess that
    held the whole body via `.content` would risk OOM (SIGKILL) on the largest
    cubes. zipfile needs a seekable file, which the temp file provides."""
    client = get_client()
    with open(dest_path, "wb") as fh, client.stream("GET", url, timeout=(_CONNECT_TIMEOUT, _READ_TIMEOUT)) as resp:
        resp.raise_for_status()
        for chunk in resp.iter_bytes(_CHUNK):
            fh.write(chunk)


def _pick_data_member(zf: zipfile.ZipFile, pid: str) -> str:
    """The data CSV is {productId}.csv; never the *_MetaData.csv companion."""
    member = f"{pid}.csv"
    if member in zf.namelist():
        return member
    cands = [
        n for n in zf.namelist()
        if n.lower().endswith(".csv") and "metadata" not in n.lower()
    ]
    if not cands:
        raise RuntimeError(f"no data CSV in zip for productId {pid}: {zf.namelist()}")
    return cands[0]


@_table_retry
def _fetch_table(asset: str, pid: str) -> None:
    """Resolve -> download -> validate -> stream inner CSV to raw, as one
    retryable unit: any transient failure re-runs from the resolve so a partial
    download is never published."""
    zip_url = _resolve_zip_url(pid)

    fd, tmp_path = tempfile.mkstemp(suffix=".zip", prefix=f"{asset}-")
    os.close(fd)
    try:
        _download_zip(zip_url, tmp_path)
        # Open BEFORE writing raw: a truncated/corrupt download raises BadZipFile
        # here (retryable) instead of silently publishing a partial table.
        with zipfile.ZipFile(tmp_path) as zf:
            member = _pick_data_member(zf, pid)
            # Stream the inner CSV (can be 1GB+ uncompressed) straight to raw,
            # never materializing it in memory or on local disk in full.
            with zf.open(member) as src, raw_writer(asset, "csv", mode="wb") as dst:
                while True:
                    chunk = src.read(_CHUNK)
                    if not chunk:
                        break
                    dst.write(chunk)
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    pid = node_id[len(SLUG) + 1:]  # strip "statistics-canada-" -> productId
    _fetch_table(asset, pid)


from constants import ENTITY_IDS

DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# Generic per-table transform: keep every StatCan column (REF_DATE, GEO, the
# table-specific dimension columns, UOM, SCALAR_FACTOR, VECTOR, COORDINATE,
# STATUS, ...), typing VALUE as DOUBLE and pinning COORDINATE to VARCHAR (it is
# a dotted coordinate string that read_csv_auto otherwise infers as DOUBLE for
# single-dimension tables). Empty VALUE strings become NULL via TRY_CAST.
_TRANSFORM_SQL = (
    'SELECT * REPLACE ('
    'TRY_CAST("VALUE" AS DOUBLE) AS "VALUE", '
    'CAST("COORDINATE" AS VARCHAR) AS "COORDINATE"'
    ') FROM "{dep}"'
)

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_TRANSFORM_SQL.format(dep=s.id),
    )
    for s in DOWNLOAD_SPECS
]
