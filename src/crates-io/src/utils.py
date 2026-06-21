"""Shared transport + extraction for the crates.io connector.

The source is a single CC0 PostgreSQL dump (``db-dump.tar.gz``, ~1.3 GB gzipped,
regenerated daily ~02:00 UTC) bundling ~15 CSV tables. We publish five Delta
tables, each from its own download node, but all five share ONE underlying
artifact: the dump. To avoid re-downloading 1.3 GB five times, the first node to
run downloads the archive into a process-shared temp cache (guarded by a file
lock and keyed by the archive's ETag); the remaining nodes reuse it. The cache
lives in the OS temp dir, so it is naturally fresh per CI container.

Each download node streams its table(s) out of the cached tar and writes them as
raw parquet with every kept column forced to ``string`` — the column set is
selected by name (the dump's CSV headers are alphabetised, not DDL order), and
all typing/casting is deferred to the SQL transforms, which are the correctness
gate.

Note: ``version_downloads`` ships only a rolling ~90-day window upstream. The
harness transform layer overwrites (it cannot merge-accumulate), so the published
``version_downloads_daily`` table is that rolling window, not a growing panel.
"""

import os
import shutil
import tempfile

try:
    import fcntl  # POSIX file lock (runner is Linux)
except ImportError:  # pragma: no cover - non-POSIX dev box
    fcntl = None

import pyarrow as pa
import pyarrow.csv as pcsv

from subsets_utils import (
    get_client,
    raw_parquet_writer,
    transient_retry,
)

DUMP_URL = "https://static.crates.io/db-dump.tar.gz"

_CACHE_DIR = os.path.join(tempfile.gettempdir(), "crates-io-db-dump")
_DUMP_PATH = os.path.join(_CACHE_DIR, "db-dump.tar.gz")
_MARKER_PATH = os.path.join(_CACHE_DIR, "version.txt")
_LOCK_PATH = os.path.join(_CACHE_DIR, "download.lock")


# --------------------------------------------------------------------------- #
# Transport
# --------------------------------------------------------------------------- #


def _current_version() -> str:
    """Cheap cache key: the dump's ETag / Last-Modified. Empty on failure —
    an empty key just means 'download once per fresh cache dir'."""
    try:
        resp = get_client().head(DUMP_URL, follow_redirects=True, timeout=30.0)
        resp.raise_for_status()
        return resp.headers.get("etag") or resp.headers.get("last-modified") or ""
    except Exception:
        return ""


@transient_retry(attempts=5, min_wait=5)
def _download_dump(dest: str) -> None:
    """Stream the dump to a scratch file (bounded memory). This is a temp
    cache file, not the raw asset layer — raw assets still go through
    subsets_utils writers below."""
    client = get_client()
    with client.stream("GET", DUMP_URL, follow_redirects=True,
                       timeout=(10.0, 600.0)) as resp:
        resp.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in resp.iter_bytes(chunk_size=1 << 20):
                f.write(chunk)


def _ensure_dump_cached() -> str:
    """Download the dump once into the shared cache and return its path.
    Concurrent nodes coordinate via an exclusive file lock; the ETag marker
    lets a node reuse an archive a sibling already fetched."""
    os.makedirs(_CACHE_DIR, exist_ok=True)
    version = _current_version()
    lock = open(_LOCK_PATH, "w")
    try:
        if fcntl is not None:
            fcntl.flock(lock, fcntl.LOCK_EX)
        if (os.path.exists(_DUMP_PATH) and os.path.getsize(_DUMP_PATH) > 0
                and os.path.exists(_MARKER_PATH)):
            with open(_MARKER_PATH) as f:
                if f.read().strip() == version:
                    print(f"  reusing cached dump (version={version!r})")
                    return _DUMP_PATH
        print(f"  downloading dump (version={version!r})...")
        partial = _DUMP_PATH + ".partial"
        _download_dump(partial)
        os.replace(partial, _DUMP_PATH)
        with open(_MARKER_PATH, "w") as f:
            f.write(version)
        print(f"  downloaded {os.path.getsize(_DUMP_PATH) / 1e9:.2f} GB")
        return _DUMP_PATH
    finally:
        if fcntl is not None:
            fcntl.flock(lock, fcntl.LOCK_UN)
        lock.close()


def extract_members(wanted: set) -> dict:
    """Stream the cached tar and copy each wanted ``data/<name>.csv`` member to
    a temp file. Returns {basename: temp_path}. Streaming keeps memory bounded
    even for the multi-GB tables; we stop once all wanted members are seen."""
    import tarfile

    path = _ensure_dump_cached()
    out = {}
    with open(path, "rb") as fh:
        tar = tarfile.open(fileobj=fh, mode="r|gz")
        for m in tar:
            if "/data/" not in m.name:
                continue
            base = m.name.rsplit("/", 1)[-1]
            if base not in wanted:
                continue
            src = tar.extractfile(m)
            fd, tmp = tempfile.mkstemp(suffix=".csv", dir=_CACHE_DIR)
            with os.fdopen(fd, "wb") as dst:
                shutil.copyfileobj(src, dst, length=1 << 20)
            out[base] = tmp
            if len(out) == len(wanted):
                break
    missing = wanted - set(out)
    if missing:
        raise RuntimeError(f"dump missing expected CSV members: {sorted(missing)}")
    return out


# A single CSV row can hold a large quoted field (e.g. a version's `features`
# jsonb or a crate readme), so the read block must exceed the biggest row or
# pyarrow raises "straddling object straddles two block boundaries".
_BLOCK_SIZE = 1 << 28  # 256 MB


def _read_options() -> pcsv.ReadOptions:
    return pcsv.ReadOptions(block_size=_BLOCK_SIZE)


def read_csv_table(csv_path: str, columns: list) -> pa.Table:
    """Read selected columns of a CSV fully into memory, all as strings."""
    convert = pcsv.ConvertOptions(
        include_columns=list(columns),
        column_types={c: pa.string() for c in columns},
    )
    parse = pcsv.ParseOptions(newlines_in_values=True)
    return pcsv.read_csv(csv_path, read_options=_read_options(),
                         parse_options=parse, convert_options=convert)


def stream_csv_to_parquet(csv_path: str, asset: str, columns: list) -> None:
    """Stream selected columns of a CSV into raw parquet (bounded memory),
    every column typed as string for a stable cross-run schema."""
    convert = pcsv.ConvertOptions(
        include_columns=list(columns),
        column_types={c: pa.string() for c in columns},
    )
    parse = pcsv.ParseOptions(newlines_in_values=True)
    reader = pcsv.open_csv(csv_path, read_options=_read_options(),
                           parse_options=parse, convert_options=convert)
    schema = reader.schema
    rows = 0
    with raw_parquet_writer(asset, schema) as w:
        for batch in reader:
            if batch.num_rows == 0:
                continue
            w.write_table(pa.Table.from_batches([batch], schema=schema))
            rows += batch.num_rows
    print(f"  {asset}: {rows:,} rows")


def cleanup(paths) -> None:
    for p in paths:
        try:
            os.unlink(p)
        except OSError:
            pass
