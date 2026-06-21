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
import io
import zipfile


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_writer,
    transient_retry,
)

SLUG = "statistics-canada"
_RESOLVE_URL = "https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/{pid}/en"


@transient_retry()
def _get(url: str):
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp


def _resolve_zip_url(pid: str) -> str:
    """Resolve a productId to its stable full-table CSV zip URL via WDS."""
    payload = _get(_RESOLVE_URL.format(pid=pid)).json()
    rec = payload[0] if isinstance(payload, list) else payload
    if not isinstance(rec, dict) or rec.get("status") != "SUCCESS" or not rec.get("object"):
        raise RuntimeError(f"WDS resolve failed for productId {pid}: {payload!r:.200}")
    return rec["object"]


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    pid = node_id[len(SLUG) + 1:]  # strip "statistics-canada-" -> productId

    zip_url = _resolve_zip_url(pid)
    resp = _get(zip_url)  # compressed zip into memory (~tens of MB); inner CSV is streamed out
    zf = zipfile.ZipFile(io.BytesIO(resp.content))

    member = f"{pid}.csv"
    if member not in zf.namelist():
        # Fall back to the data CSV (anything that is not the *_MetaData.csv companion).
        cands = [
            n for n in zf.namelist()
            if n.lower().endswith(".csv") and "metadata" not in n.lower()
        ]
        if not cands:
            raise RuntimeError(f"no data CSV in zip for productId {pid}: {zf.namelist()}")
        member = cands[0]

    # Stream the inner CSV (can be 1GB+ uncompressed) to raw without materializing it.
    with zf.open(member) as src, raw_writer(asset, "csv", mode="wb") as dst:
        while True:
            chunk = src.read(1 << 20)
            if not chunk:
                break
            dst.write(chunk)


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
