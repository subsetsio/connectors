"""Statistics Canada connector.

One published Delta table per accepted StatCan data cube (productId). Access is
the WDS bulk full-table CSV path (research mechanism `bulk_csv`): the
getFullTableDownloadCSV resolver returns a stable per-table zip URL; the zip
holds {productId}.csv (full history, all coordinates) plus a metadata CSV. We
stream the inner data CSV straight to raw (memory-bounded — the inner CSV can be
1GB+ uncompressed) and a generic DuckDB transform types the VALUE column and
publishes.

Fetch shape: stateless full re-pull. Each cube is small-to-large but fetchable
in one request; the bulk zip always carries the complete table, so there is no
watermark/cursor — every run overwrites with the current full table, picking up
revisions for free. No auth (open service). WDS documents 50 req/s server-wide,
25 req/s per IP; node specs run in separate processes so per-process backoff on
429/5xx (below) is the pacing mechanism.
"""
import os
import tempfile
import zipfile


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    get_client,
    raw_writer,
    transient_retry,
)

SLUG = "statistics-canada"
_RESOLVE_URL = "https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/{pid}/en"
_CHUNK = 1 << 20  # 1 MiB
# Connect fast; allow a long *per-chunk* read window. Because we stream the body
# chunk-by-chunk the read timeout applies to each read, never to the whole (1GB+)
# transfer — so a steady-but-slow large download won't trip it, while a genuinely
# stalled socket still raises a transient ReadTimeout that transient_retry retries.
_TIMEOUT = (30.0, 300.0)


@transient_retry()
def _resolve_zip_url(pid: str) -> str:
    """Resolve a productId to its stable full-table CSV zip URL via WDS."""
    resp = get(_RESOLVE_URL.format(pid=pid), timeout=(30.0, 120.0))
    resp.raise_for_status()
    payload = resp.json()
    rec = payload[0] if isinstance(payload, list) else payload
    if not isinstance(rec, dict) or rec.get("status") != "SUCCESS" or not rec.get("object"):
        raise RuntimeError(f"WDS resolve failed for productId {pid}: {payload!r:.200}")
    return rec["object"]


@transient_retry()
def _download_zip(url: str, dest_path: str) -> None:
    """Stream the full-table zip to a local scratch file.

    The zip stays on disk (compressed, tens-to-hundreds of MB) rather than in
    RAM — a spawn-subprocess that buffered the whole body via `.content` would
    risk OOM (SIGKILL) on the largest cubes. zipfile needs a seekable file,
    which the temp file provides. Re-truncates on each retry attempt.
    """
    client = get_client()
    with open(dest_path, "wb") as fh, client.stream("GET", url, timeout=_TIMEOUT) as resp:
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


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    pid = node_id[len(SLUG) + 1:]  # strip "statistics-canada-" -> productId

    zip_url = _resolve_zip_url(pid)

    fd, tmp_path = tempfile.mkstemp(suffix=".zip", prefix=f"{asset}-")
    os.close(fd)
    try:
        _download_zip(zip_url, tmp_path)
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
