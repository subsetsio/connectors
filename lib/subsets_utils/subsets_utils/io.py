"""Data I/O for raw assets, state files, and Delta tables.

Single code path for both local and cloud storage. All raw + state I/O
is routed through fsspec via `get_fs(uri)` — local paths use the local
filesystem, `s3://` URIs use s3fs. The primitives below are a thin
shell over fsspec; callers see a uniform byte-level API.

In cloud, `raw_uri()` / `state_uri()` return `s3://` URIs directly, so
io.py streams reads/writes straight to R2 via s3fs multipart upload —
there is no hydrate/flush bookend. In local mode they return local paths.

Raw manifest: every raw write stages a per-connector manifest entry AFTER
the object write (see raw_manifest.py — the parent orchestrator commits a
node's staged entries when the node succeeds), and every raw read resolves
through the manifest first, falling back to the legacy run-scoped path when
the manifest has no entry (back-compat for pre-manifest connectors). This is
what lets raw survive across runs: a maintain-skipped fetch's prior objects
stay addressable, and `raw_asset_exists(max_age_days=N)` reads real
freshness (`fetched_at`) instead of probing an empty fresh run dir.

Streaming: for datasets that don't fit in memory use `raw_writer()`
(generic byte stream) or `raw_parquet_writer()` (row-group streaming
ParquetWriter). Both are context managers that yield a file-like
object or a writer, bounded by fsspec's block size.
"""

import io
import json
import gzip
import os
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

import pyarrow as pa
import pyarrow.parquet as pq

from . import raw_manifest, tracking
from .config import get_fs, raw_uri, state_uri
from .storage import backend


# =============================================================================
# URI dispatch via fsspec
# =============================================================================

def _write_bytes(uri: str, data: bytes) -> None:
    """Write bytes to a URI (s3:// or local path). Delegates to StorageBackend."""
    backend.write_bytes(uri, data)


def _read_bytes(uri: str) -> Optional[bytes]:
    """Read bytes from a URI. Returns None if not found. Delegates to StorageBackend."""
    return backend.read_bytes(uri)


def _exists(uri: str) -> bool:
    """Check if a URI exists. Delegates to StorageBackend."""
    return backend.exists(uri)


def _delete(uri: str) -> None:
    """Delete a URI. No-op if already absent. Delegates to StorageBackend."""
    backend.delete(uri)


# =============================================================================
# State files (small JSON, per-asset)
# =============================================================================

def _load_state_raw(asset: str) -> dict:
    """Load state including underscore-prefixed reserved keys (e.g. _metadata).
    Internal: used by record_completion and save_state's merge path."""
    uri = state_uri(asset)
    data = _read_bytes(uri)
    if not data:
        return {}
    return json.loads(data.decode("utf-8"))


def load_state(asset: str) -> dict:
    """Load state for an asset. Returns empty dict if not found.

    Reserved underscore-prefixed keys (e.g. `_metadata`) are stripped from
    the returned dict — they are managed by the orchestrator, not by fetch
    fns. This means the common load-modify-save pattern stays safe:

        state = load_state(asset)
        state["watermark"] = new_watermark
        save_state(asset, state)

    won't trip the reserved-prefix guard on save.
    """
    raw = _load_state_raw(asset)
    return {k: v for k, v in raw.items() if not k.startswith("_")}


def save_state(asset: str, state_data: dict) -> str:
    """Save state for an asset. Returns the URI.

    Fetch-fn-managed state only. Underscore-prefixed keys are reserved for
    the orchestrator (see `record_completion`) — passing one here raises.
    Existing `_metadata` on disk (e.g. `code_hash` written post-success)
    is preserved across this write; only `updated_at` and `run_id` get
    refreshed each save.
    """
    import os
    for k in state_data:
        if isinstance(k, str) and k.startswith("_"):
            raise ValueError(
                f"reserved key in save_state user dict: {k!r}. "
                "Underscore-prefixed keys are managed by the orchestrator."
            )

    existing = _load_state_raw(asset)
    existing_meta = existing.get("_metadata", {}) if isinstance(existing.get("_metadata"), dict) else {}

    merged_meta = {
        **existing_meta,
        "updated_at": datetime.now().isoformat(),
        "run_id": os.environ.get("RUN_ID", "unknown"),
    }
    payload = {
        **state_data,
        "_metadata": merged_meta,
    }
    uri = state_uri(asset)
    _write_bytes(uri, json.dumps(payload, indent=2).encode("utf-8"))
    tracking.record_state_change(asset, existing, payload)
    return uri


def record_completion(asset: str, code_hash: str | None) -> str:
    """Stamp `_metadata.code_hash` for `asset` after a successful materialization.

    Called by the orchestrator post-success — not by fetch fns. Bypasses the
    `save_state` reserved-prefix guard because it operates ENTIRELY under the
    reserved namespace; fetch-fn-managed keys are preserved as-is.

    A `None` hash means "compute failed; we don't know what produced this state"
    and is recorded honestly rather than papering over it.
    """
    import os
    existing = _load_state_raw(asset)
    existing_meta = existing.get("_metadata", {}) if isinstance(existing.get("_metadata"), dict) else {}

    merged_meta = {
        **existing_meta,
        "code_hash": code_hash,
        "updated_at": datetime.now().isoformat(),
        "run_id": os.environ.get("RUN_ID", "unknown"),
    }
    user_keys = {k: v for k, v in existing.items() if not (isinstance(k, str) and k.startswith("_"))}
    payload = {
        **user_keys,
        "_metadata": merged_meta,
    }
    uri = state_uri(asset)
    _write_bytes(uri, json.dumps(payload, indent=2).encode("utf-8"))
    tracking.record_state_change(asset, existing, payload)
    return uri


# =============================================================================
# Raw files (text/binary blobs — CSV, XML, ZIP, etc.)
# =============================================================================

def save_raw_file(content: str | bytes, asset_id: str, extension: str = "txt", *, entity_id: str | None = None, fragment: str | None = None) -> str:
    """Save a raw file. Accepts str or bytes.

    entity_id (optional): namespaces the path under data/raw/<entity_id>/.
    Used by meta-authored connectors (entity-prefix layout). When None
    (default), legacy flat layout.

    fragment (optional): None (default) writes the whole asset — the manifest's
    "full" fragment, replacing every previously recorded fragment. A named
    fragment writes `<asset_id>-<fragment>.<ext>` and replaces only that key,
    leaving sibling fragments intact (incremental partitions of one asset)."""
    data = content.encode("utf-8") if isinstance(content, str) else content
    oid = raw_manifest.object_id(asset_id, fragment)
    uri = raw_uri(oid, extension, entity_id=entity_id)
    _write_bytes(uri, data)
    raw_manifest.stage_write(asset_id, extension, uri, size=len(data),
                             hash=raw_manifest.content_hash(data),
                             entity_id=entity_id, fragment=fragment)
    print(f"  -> Saved {oid}.{extension}")
    return uri


def load_raw_file(asset_id: str, extension: str = "txt", *, binary: bool = False, entity_id: str | None = None) -> str | bytes:
    """Load a raw file.

    Args:
        asset_id: Asset name.
        extension: File extension.
        binary: If True, always return bytes. If False (default), attempt
            UTF-8 decode and return str on success, bytes on failure.
            Set binary=True for xlsx/zip/parquet or any file where you
            need deterministic bytes — the decode fallback is unreliable
            when a binary payload happens to be ASCII-only.
        entity_id: Optional. If set, looks under data/raw/<entity_id>/ —
            meta entity-prefix layout. Default None = legacy flat path.

    Resolution: the connector's raw manifest first (may point into a prior
    run's dir); the run-scoped/local path when the manifest has no entry.
    """
    from .tracking import record_read
    uri = (raw_manifest.resolve_read_uri(asset_id, extension, entity_id=entity_id)
           or raw_uri(asset_id, extension, entity_id=entity_id))
    data = _read_bytes(uri)
    if data is None:
        raise FileNotFoundError(f"Raw asset '{asset_id}.{extension}' not found at {uri}")
    record_read(f"raw/{(entity_id + '/') if entity_id else ''}{asset_id}.{extension}")
    if binary:
        return data
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data


# =============================================================================
# Raw JSON (with optional gzip compression)
# =============================================================================

def save_raw_json(data, asset_id: str, compress: bool = False, *, entity_id: str | None = None, fragment: str | None = None) -> str:
    """Save raw JSON data, optionally gzip-compressed.

    entity_id: namespace under data/raw/<entity_id>/ (meta entity-prefix).
    Default None = legacy flat layout.
    fragment: None (default) = the whole asset ("full", replaces all recorded
    fragments); a name = replace just that fragment (see save_raw_file)."""
    if compress:
        ext = "json.gz"
        buf = io.BytesIO()
        with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
            gz.write(json.dumps(data).encode("utf-8"))
        content = buf.getvalue()
    else:
        ext = "json"
        content = json.dumps(data, indent=2).encode("utf-8")
    oid = raw_manifest.object_id(asset_id, fragment)
    uri = raw_uri(oid, ext, entity_id=entity_id)
    _write_bytes(uri, content)
    raw_manifest.stage_write(asset_id, ext, uri, size=len(content),
                             hash=raw_manifest.content_hash(content),
                             entity_id=entity_id, fragment=fragment)
    print(f"  -> Saved {oid}.{ext}")
    return uri


def load_raw_json(asset_id: str, *, entity_id: str | None = None):
    """Load raw JSON. Auto-detects compression (tries .json then .json.gz).
    Resolves via the raw manifest first; falls back to the run-scoped path.

    entity_id: read from data/raw/<entity_id>/ (meta entity-prefix layout)."""
    from .tracking import record_read
    for ext in ("json", "json.gz"):
        uri = (raw_manifest.resolve_read_uri(asset_id, ext, entity_id=entity_id)
               or raw_uri(asset_id, ext, entity_id=entity_id))
        data = _read_bytes(uri)
        if data is None:
            continue
        record_read(f"raw/{(entity_id + '/') if entity_id else ''}{asset_id}.{ext}")
        if ext == "json.gz":
            with gzip.GzipFile(fileobj=io.BytesIO(data), mode="rb") as gz:
                return json.load(gz)
        return json.loads(data.decode("utf-8"))
    raise FileNotFoundError(f"Raw JSON asset '{asset_id}' not found.")


# =============================================================================
# Raw NDJSON (newline-delimited JSON, zstd-compressed by default)
#
# Use when records are heterogeneous, nested, or types drift across batches —
# anything where declaring a parquet schema would be brittle. For tabular data
# with stable column types, prefer save_raw_parquet.
# =============================================================================

_NDJSON_EXT = {"zstd": "ndjson.zst", "gzip": "ndjson.gz", None: "ndjson"}


def save_raw_ndjson(rows, asset_id: str, *, compression: str | None = "zstd", fragment: str | None = None) -> str:
    """Save records as NDJSON (one JSON object per line). Default: zstd.

    For datasets that fit in memory. For larger ones use `raw_writer(asset,
    "ndjson.gz", mode="wt", compression="gzip")` and stream line-by-line, or
    the zstd equivalent if zstandard is available in the runtime.

    Args:
        rows: Iterable of JSON-serializable dicts.
        asset_id: Logical asset name.
        compression: "zstd" (default), "gzip", or None.
        fragment: None (default) = the whole asset ("full", replaces all
            recorded fragments); a name = replace just that fragment.
    """
    if compression not in _NDJSON_EXT:
        raise ValueError(f"compression must be 'zstd', 'gzip', or None; got {compression!r}")
    ext = _NDJSON_EXT[compression]

    n = 0
    if compression is None:
        out = io.BytesIO()
        for row in rows:
            out.write(json.dumps(row, separators=(",", ":")).encode("utf-8"))
            out.write(b"\n")
            n += 1
        content = out.getvalue()
    else:
        comp_buf = pa.BufferOutputStream()
        with pa.CompressedOutputStream(comp_buf, compression=compression) as out:
            for row in rows:
                out.write(json.dumps(row, separators=(",", ":")).encode("utf-8"))
                out.write(b"\n")
                n += 1
        content = comp_buf.getvalue().to_pybytes()

    oid = raw_manifest.object_id(asset_id, fragment)
    uri = raw_uri(oid, ext)
    _write_bytes(uri, content)
    raw_manifest.stage_write(asset_id, ext, uri, size=len(content),
                             hash=raw_manifest.content_hash(content),
                             fragment=fragment)
    print(f"  -> Saved {oid}.{ext} ({n:,} records)")
    return uri


def load_raw_ndjson(asset_id: str) -> list[dict]:
    """Load NDJSON records. Auto-detects compression by trying .zst, .gz, then
    plain. Resolves via the raw manifest first; falls back to the run-scoped path."""
    from .tracking import record_read
    for compression, ext in (("zstd", "ndjson.zst"), ("gzip", "ndjson.gz"), (None, "ndjson")):
        uri = (raw_manifest.resolve_read_uri(asset_id, ext)
               or raw_uri(asset_id, ext))
        data = _read_bytes(uri)
        if data is None:
            continue
        record_read(f"raw/{asset_id}.{ext}")
        if compression is None:
            text = data.decode("utf-8")
        else:
            stream = pa.CompressedInputStream(pa.BufferReader(pa.py_buffer(data)), compression=compression)
            text = stream.read().decode("utf-8")
        return [json.loads(line) for line in text.splitlines() if line]
    raise FileNotFoundError(f"Raw NDJSON asset '{asset_id}' not found.")


def delete_raw_file(asset_id: str, extension: str = "parquet", *, entity_id: str | None = None) -> None:
    """Delete a raw asset by (asset_id, extension). No-op if absent.

    Symmetric with `save_raw_*` — addresses by id, works in cloud + dev.
    Also stages removal of the asset's raw-manifest entry (committed when the
    node succeeds), so readers stop resolving to prior runs' objects.
    """
    _delete(raw_uri(asset_id, extension, entity_id=entity_id))
    raw_manifest.stage_delete(asset_id, extension, entity_id=entity_id)


# =============================================================================
# Raw Parquet (PyArrow tables)
# =============================================================================

def save_raw_parquet(data: pa.Table, asset_id: str, *, fragment: str | None = None) -> str:
    """Save a PyArrow table as Parquet.

    fragment: None (default) = the whole asset ("full", replaces all recorded
    fragments); a name = replace just that fragment (see save_raw_file)."""
    if hasattr(data, "read_all"):
        data = data.read_all()
    buf = io.BytesIO()
    pq.write_table(data, buf, compression="zstd")
    content = buf.getvalue()
    oid = raw_manifest.object_id(asset_id, fragment)
    uri = raw_uri(oid, "parquet")
    _write_bytes(uri, content)
    raw_manifest.stage_write(asset_id, "parquet", uri, size=len(content),
                             hash=raw_manifest.content_hash(content),
                             fragment=fragment)
    print(f"  -> Saved {oid}.parquet ({data.num_rows:,} rows)")
    return uri


def load_raw_parquet(asset_id: str) -> pa.Table:
    """Load a Parquet file as PyArrow table. Resolves via the raw manifest
    first; falls back to the run-scoped path."""
    from .tracking import record_read
    uri = raw_manifest.resolve_read_uri(asset_id, "parquet") or raw_uri(asset_id, "parquet")
    data = _read_bytes(uri)
    if data is None:
        raise FileNotFoundError(f"Raw parquet '{asset_id}' not found at {uri}")
    record_read(f"raw/{asset_id}.parquet")
    return pq.read_table(io.BytesIO(data))


@contextmanager
def raw_parquet_localpath(asset_id: str):
    """Context manager yielding a local filesystem path to a raw parquet.

    In dev mode: yields the dev path directly — no copy.
    In cloud mode: streams the remote parquet to a tempfile and yields
    that path; the file is deleted on exit.

    Use this when you need a file path for tools like DuckDB that read
    parquet by path rather than loading bytes into memory. The compressed
    parquet on disk is typically 5-10× smaller than its decompressed
    Arrow representation, so streaming queries against the path stay
    memory-bounded even when load_raw_parquet() would OOM.
    """
    from .tracking import record_read
    import tempfile
    import os as _os

    uri = raw_manifest.resolve_read_uri(asset_id, "parquet") or raw_uri(asset_id, "parquet")
    record_read(f"raw/{asset_id}.parquet")

    if not uri.startswith("s3://"):
        local = Path(uri)
        if local.exists():
            yield str(local)
            return
        raise FileNotFoundError(f"Raw parquet '{asset_id}' not found at {uri}")

    fs = get_fs(uri)
    tmp = tempfile.NamedTemporaryFile(
        suffix=f".{asset_id}.parquet", delete=False
    )
    tmp.close()
    try:
        with fs.open(uri, "rb") as src, open(tmp.name, "wb") as dst:
            while True:
                chunk = src.read(16 * 1024 * 1024)
                if not chunk:
                    break
                dst.write(chunk)
        yield tmp.name
    finally:
        try:
            _os.unlink(tmp.name)
        except OSError:
            pass


# =============================================================================
# Streaming helpers — for datasets too big to fit in memory
#
# These open an fsspec file handle via `get_fs(uri)`. Local paths get auto
# parent-dir creation; s3:// URIs stream via multipart upload.
# =============================================================================

def _written_size(fs, uri: str) -> int | None:
    """Best-effort object size after a streamed write (manifest metadata)."""
    try:
        info = fs.info(uri)
        size = info.get("size") if isinstance(info, dict) else None
        return int(size) if size is not None else None
    except Exception:
        return None


@contextmanager
def raw_writer(
    asset_id: str,
    extension: str = "txt",
    *,
    mode: str = "wb",
    compression: str | None = None,
    encoding: str | None = "utf-8",
    fragment: str | None = None,
):
    """Streaming writer for a raw asset. Context manager yielding a file handle.

    Use when the content doesn't fit in memory. Writes go through fsspec,
    so s3:// URIs stream via multipart upload and local paths get parent
    dirs auto-created. Supports native gzip/bz2/xz compression.

    Args:
        asset_id: Logical asset name (same as save_raw_*).
        extension: File extension (e.g. "ndjson.gz", "csv").
        mode: File mode — "wb" for bytes (default), "wt" for text.
        compression: "gzip", "bz2", "xz", or None. Matches fsspec.
        encoding: Text encoding when mode="wt". Ignored for binary.
        fragment: None (default) = the whole asset ("full"); a name =
            replace just that fragment in the raw manifest. Streamed writes
            record no content hash (bytes never pass through memory whole).

    Example:
        with raw_writer("big_dump", "ndjson.gz", mode="wt", compression="gzip") as f:
            for row in stream:
                f.write(json.dumps(row) + "\\n")
    """
    oid = raw_manifest.object_id(asset_id, fragment)
    uri = raw_uri(oid, extension)
    fs = get_fs(uri)
    open_kwargs = {}
    if "t" in mode:
        open_kwargs["encoding"] = encoding
    if compression is not None:
        open_kwargs["compression"] = compression
    with fs.open(uri, mode=mode, **open_kwargs) as f:
        yield f
    raw_manifest.stage_write(asset_id, extension, uri,
                             size=_written_size(fs, uri), hash=None,
                             fragment=fragment)
    print(f"  -> Saved {oid}.{extension}")


@contextmanager
def raw_reader(
    asset_id: str,
    extension: str = "txt",
    *,
    mode: str = "rb",
    compression: str | None = None,
    encoding: str | None = "utf-8",
):
    """Streaming reader for a raw asset. Symmetric with raw_writer().
    Resolves via the raw manifest first; falls back to the run-scoped path."""
    from .tracking import record_read
    uri = (raw_manifest.resolve_read_uri(asset_id, extension)
           or raw_uri(asset_id, extension))

    fs = get_fs(uri)
    open_kwargs = {}
    if "t" in mode:
        open_kwargs["encoding"] = encoding
    if compression is not None:
        open_kwargs["compression"] = compression
    with fs.open(uri, mode=mode, **open_kwargs) as f:
        yield f
    record_read(f"raw/{asset_id}.{extension}")


@contextmanager
def raw_parquet_writer(asset_id: str, schema: pa.Schema, *, compression: str = "zstd", fragment: str | None = None):
    """Streaming Parquet writer yielding a `pq.ParquetWriter`.

    Bounded memory for arbitrarily large datasets — call `write_table()`
    or `write_batch()` inside the `with` block, and the writer flushes
    row groups as they grow. Works for both local and s3:// URIs.

    fragment: None (default) = the whole asset ("full"); a name = replace
    just that fragment in the raw manifest. Streamed writes record no
    content hash.

    Example:
        with raw_parquet_writer("wiki_dump", schema) as w:
            for batch in stream_wikipedia():
                w.write_batch(batch)
    """
    oid = raw_manifest.object_id(asset_id, fragment)
    uri = raw_uri(oid, "parquet")
    fs = get_fs(uri)
    with fs.open(uri, "wb") as f:
        writer = pq.ParquetWriter(f, schema, compression=compression)
        try:
            yield writer
        finally:
            writer.close()
    raw_manifest.stage_write(asset_id, "parquet", uri,
                             size=_written_size(fs, uri), hash=None,
                             fragment=fragment)
    print(f"  -> Saved {oid}.parquet (streamed)")


# =============================================================================
# Listing & existence checks
# =============================================================================

def list_raw_files(pattern: str) -> list[str]:
    """List raw files in the RUN-SCOPED raw dir matching a glob pattern.

    For POST-DOWNLOAD ENUMERATION ONLY — health tests (tests_download.py)
    globbing the batches their own run just wrote, dev smoke scripts. This is
    a physical directory listing, NOT the commit log: it can return objects
    the raw manifest discarded (a failed leg's writes). NEVER derive a fetch
    fn's skip/done-set from it — an uncommitted object skipped as "done"
    becomes a silent hole in the published table, because transforms resolve
    manifest-first. Skip decisions use `list_raw_fragments`.

    Args:
        pattern: Glob like "items/*.json.gz" — relative to the raw dir.

    Returns:
        Sorted list of relative paths.
    """
    # Probe raw_uri to get the connector's raw dir (s3:// or local). The
    # "__probe__" asset is never created — raw_uri only builds the path.
    probe = raw_uri("__probe__", "__")
    base_uri = probe.rsplit("/", 1)[0]

    if base_uri.startswith("s3://"):
        fs = get_fs(base_uri)
        # The fsspec instance is process-cached and s3fs caches directory
        # listings, so a listing taken earlier in this process (e.g. in the
        # orchestrator while the DAG was still writing) would hide objects
        # written since. A physical listing must reflect the store as it is
        # NOW — drop the cached listings before globbing.
        fs.invalidate_cache()
        try:
            matches = fs.glob(f"{base_uri}/{pattern}")
        except FileNotFoundError:
            return []
        # s3fs returns keys without "s3://bucket/" prefix
        from urllib.parse import urlparse
        s3_prefix = urlparse(base_uri).path.lstrip("/") + "/"
        bucket = urlparse(base_uri).netloc
        rels = [
            m[len(f"{bucket}/{s3_prefix}"):] if m.startswith(f"{bucket}/{s3_prefix}") else m[len(s3_prefix):]
            for m in matches
        ]
        # `.manifest/` holds per-node raw-manifest staging files, not raw data.
        return sorted(r for r in rels if not r.startswith(".manifest"))

    raw_dir = Path(base_uri)
    if not raw_dir.exists():
        return []
    return sorted(
        str(p.relative_to(raw_dir)) for p in raw_dir.glob(pattern)
        if not str(p.relative_to(raw_dir)).startswith(".manifest")
    )


def list_raw_fragments(asset_id: str, extension: str = "parquet", *,
                       entity_id: str | None = None) -> dict[str, dict]:
    """Live fragments of a raw asset per the COMMIT LOG — the committed raw
    manifest overlaid with this process's own pending writes.

    Returns {fragment: {"path", "size", "run_id", "fetched_at", ...}} where
    "full" is the whole-asset fragment; {} when the manifest has no entry for
    (asset_id, extension).

    This is the correct basis for incremental skip decisions ("which windows
    are already fetched"): an object the manifest does not reference does not
    exist — a failed leg's unreferenced writes must be refetched, or transforms
    (which resolve manifest-first) silently miss them. Never derive a done-set
    from directory listings.

    Scope the done-set to the current run for continuation-leg resume (each
    completed leg commits, so prior legs' fragments are visible here):

        frags = list_raw_fragments(node_id, "csv.gz")
        done = {f for f, m in frags.items()
                if m.get("run_id") == os.environ.get("RUN_ID", "unknown")}

    Drop the run_id filter (or filter on fetched_at) for cross-run incremental
    policies.
    """
    entry = raw_manifest.asset_entry(asset_id, extension, entity_id=entity_id)
    if not entry:
        return {}
    return {k: dict(v) for k, v in (entry.get("fragments") or {}).items()
            if isinstance(v, dict)}


def raw_asset_exists(asset_id: str, ext: str = "parquet", max_age_days: int | None = None, *, entity_id: str | None = None) -> bool:
    """Check if a raw asset exists. Optionally check it is fresh enough.

    Resolution: the raw manifest first — its entry spans runs, so a
    MaintainSpec freshness check works in cloud even though each run's raw
    dir starts empty. `max_age_days` is judged against the entry's newest
    fragment `fetched_at`. Only when the manifest has no entry does this fall
    back to probing the run-scoped/local path (s3 `fs.info` / file mtime).

    Args:
        max_age_days: If set, returns False if the asset is older than this many days.
        entity_id: Optional. If set, looks under data/raw/<entity_id>/ —
            meta entity-prefix layout. Default None = legacy flat path.
    """
    entry = raw_manifest.asset_entry(asset_id, ext, entity_id=entity_id)
    if entry is not None:
        if max_age_days is None:
            return True
        newest = raw_manifest.newest_fetched_at(entry)
        if newest is None:
            return True  # entry exists, age unknown — assume fresh
        return (datetime.now(timezone.utc) - newest) < timedelta(days=max_age_days)

    uri = raw_uri(asset_id, ext, entity_id=entity_id)

    if uri.startswith("s3://"):
        fs = get_fs(uri)
        if not fs.exists(uri):
            return False
        if max_age_days is None:
            return True
        try:
            info = fs.info(uri)
        except FileNotFoundError:
            return False
        mtime = info.get("LastModified") or info.get("mtime")
        if mtime is None:
            return True  # existence confirmed, age unknown — assume fresh
        if hasattr(mtime, "tzinfo") and mtime.tzinfo is not None:
            now = datetime.now(mtime.tzinfo)
        else:
            now = datetime.now()
        return (now - mtime) < timedelta(days=max_age_days)

    # Local dev: check local dev dir.
    p = Path(uri)
    if not p.exists():
        return False
    if max_age_days is not None:
        age = datetime.now() - datetime.fromtimestamp(p.stat().st_mtime)
        return age < timedelta(days=max_age_days)
    return True
