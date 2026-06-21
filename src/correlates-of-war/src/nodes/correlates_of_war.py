"""Correlates of War — connector node module.

Mechanism: bulk_download. Each rank-accepted entity maps (see src/constants.py)
to one CSV living either as a bare file or inside a (sometimes nested) ZIP under
https://correlatesofwar.org/wp-content/uploads/. There is no incremental API —
the files are static, versioned artefacts, re-fetched in full each run
(stateless full re-pull; tens of MB total, the IGO dyad file dominates at
~800MB uncompressed).

Fetch shape (one generic `fetch_one` over the entity union):
  1. download the archive over HTTPS (subsets_utils.get),
  2. extract the target CSV member to a temp file,
  3. stream it through DuckDB CSV -> parquet (auto-typed) with bounded memory.

Two source quirks, both handled here:
  * TLS: correlatesofwar.org serves an incomplete certificate chain, so generic
    verification fails. We install a verify-disabled httpx client into
    subsets_utils.http_client once (these are public, non-sensitive academic
    files; research flagged this).
  * Encoding: most files are UTF-8, a few are Windows-1252 (e.g. a 0x92 smart
    quote) which DuckDB's strict reader rejects. We validate UTF-8 streaming and
    transcode the rare offender to UTF-8 before handing the path to DuckDB.

Transforms publish one Delta table per subset as a thin `SELECT *` over the
auto-typed raw parquet — DuckDB has already inferred column types from the whole
file (sample_size=-1), so the published tables are properly typed.
"""

import codecs
import io
import os
import tempfile
import zipfile

import duckdb

from subsets_utils import NodeSpec, SqlNodeSpec, get, transient_retry, raw_parquet_writer
from constants import DOWNLOADS, BASE

PREFIX = "correlates-of-war-"

_http_ready = False


def _ensure_http():
    """Install a verify-disabled shared httpx client (once per process).

    correlatesofwar.org omits an intermediate cert, so default verification
    fails on an otherwise-valid public file host. All requests still flow
    through subsets_utils.get for logging/retry.
    """
    global _http_ready
    if _http_ready:
        return
    import httpx
    import subsets_utils.http_client as hc
    if hc._client is not None:
        hc._client.close()
    hc._client = httpx.Client(
        timeout=httpx.Timeout(180.0),
        headers={"User-Agent": "subsets-correlates-of-war/1.0"},
        follow_redirects=True,
        verify=False,
    )
    _http_ready = True


@transient_retry()
def _download(filename: str) -> bytes:
    _ensure_http()
    resp = get(BASE + filename, timeout=180.0)
    resp.raise_for_status()
    return resp.content


def _extract_csv_bytes(archive: str, member, blob: bytes) -> bytes:
    """Return the raw CSV bytes for an entity given the downloaded archive."""
    if member is None:
        return blob  # bare .csv download
    if "!!" in member:  # csv inside a zip nested inside the outer zip
        inner_zip_path, inner_csv = member.split("!!", 1)
        with zipfile.ZipFile(io.BytesIO(blob)) as outer:
            inner_blob = outer.read(inner_zip_path)
        with zipfile.ZipFile(io.BytesIO(inner_blob)) as inner:
            return inner.read(inner_csv)
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        return z.read(member)


def _is_utf8(path: str) -> bool:
    """Stream-validate UTF-8 without loading the whole file into memory."""
    dec = codecs.getincrementaldecoder("utf-8")()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1 << 20)
            if not chunk:
                break
            try:
                dec.decode(chunk)
            except UnicodeDecodeError:
                return False
    try:
        dec.decode(b"", final=True)
    except UnicodeDecodeError:
        return False
    return True


def _transcode_to_utf8(src: str, dst: str):
    """Transcode a Windows-1252/Latin-1 CSV to UTF-8 in bounded memory.

    cp1252 is single-byte, so chunk boundaries are safe; undefined bytes are
    replaced rather than raising.
    """
    with open(src, "rb") as fin, open(dst, "w", encoding="utf-8", newline="") as fout:
        while True:
            chunk = fin.read(1 << 20)
            if not chunk:
                break
            fout.write(chunk.decode("cp1252", errors="replace"))


def _csv_to_parquet(csv_path: str, asset: str):
    """Stream a CSV file through DuckDB into an auto-typed raw parquet."""
    con = duckdb.connect()
    try:
        lit = csv_path.replace("'", "''")
        sql = (
            f"SELECT * FROM read_csv('{lit}', header=true, sample_size=-1, "
            f"null_padding=true, ignore_errors=false, encoding='utf-8')"
        )
        reader = con.execute(sql).fetch_record_batch(200_000)
        schema = reader.schema
        rows = 0
        with raw_parquet_writer(asset, schema) as writer:
            for batch in reader:
                if batch.num_rows:
                    writer.write_batch(batch)
                    rows += batch.num_rows
        if rows == 0:
            raise ValueError(f"{asset}: CSV parsed to 0 rows")
    finally:
        con.close()


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the raw asset name
    entity = node_id[len(PREFIX):]
    archive, member = DOWNLOADS[entity]
    blob = _download(archive)
    csv_bytes = _extract_csv_bytes(archive, member, blob)

    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "data.csv")
        with open(src, "wb") as f:
            f.write(csv_bytes)
        del blob, csv_bytes  # free memory before DuckDB scans the (possibly large) file

        if _is_utf8(src):
            csv_path = src
        else:
            csv_path = os.path.join(tmp, "data.utf8.csv")
            _transcode_to_utf8(src, csv_path)

        _csv_to_parquet(csv_path, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}{eid}", fn=fetch_one, kind="download")
    for eid in DOWNLOADS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
