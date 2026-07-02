"""Delta table operations: merge, overwrite, append.

Simple, explicit API for writing to Delta tables.
No hidden defaults. No escape hatches.
"""

import os
from dataclasses import dataclass
from typing import Union
import pyarrow as pa
from deltalake import write_deltalake, DeltaTable, CommitProperties
try:
    from deltalake.exceptions import TableNotFoundError
except ImportError:
    try:
        from deltalake import TableNotFoundError  # older deltalake
    except ImportError:
        TableNotFoundError = None  # fallback: we'll handle by exception type name

from .config import subsets_uri
from .storage import backend
from .tracking import record_write


def _is_table_not_found(exc: Exception) -> bool:
    """Distinguish 'table does not exist yet' from other Delta errors."""
    if TableNotFoundError is not None and isinstance(exc, TableNotFoundError):
        return True
    # Fallback string match for deltalake versions without a typed exception
    msg = str(exc).lower()
    return "not a delta table" in msg or "no such file" in msg or "does not exist" in msg


def _run_commit_properties() -> CommitProperties | None:
    """Build CommitProperties with run context for Delta commits.

    Embeds run_id, connector name, and GitHub Actions metadata into the
    Delta Lake commitInfo so the server can extract lineage from the log.
    Returns None if no run context is available (e.g. ad-hoc local writes).
    """
    meta = {}
    for env_key, meta_key in [
        ("RUN_ID", "subsets.run_id"),
        ("CONNECTOR_NAME", "subsets.connector"),
        ("GITHUB_RUN_ID", "subsets.github_run_id"),
    ]:
        val = os.environ.get(env_key)
        if val:
            meta[meta_key] = val

    gh_run_id = os.environ.get("GITHUB_RUN_ID")
    gh_repo = os.environ.get("GITHUB_REPOSITORY")
    if gh_run_id and gh_repo:
        meta["subsets.github_run_url"] = (
            f"https://github.com/{gh_repo}/actions/runs/{gh_run_id}"
        )

    gh_sha = os.environ.get("GITHUB_SHA")
    if gh_sha:
        meta["subsets.git_commit"] = gh_sha

    return CommitProperties(custom_metadata=meta) if meta else None


@dataclass
class WriteResult:
    uri: str
    version: int
    hash: str
    rows: int


# ---- Delta-safe schema normalization ---------------------------------------
#
# Delta Lake's type system has no TIME, DURATION, HALF_FLOAT, NULL or INTERVAL
# type — deltalake rejects a write containing any of them, at any nesting
# depth, with "Invalid data type for Delta Lake: Time64(µs)" (unsigned ints
# and large_string/large_binary ARE accepted; verified against deltalake 1.6).
# Every subset write funnels through merge/overwrite/append below, so
# normalizing HERE — not in per-connector SQL — means no connector can ever
# hit that error again (e.g. a DuckDB transform selecting a TIME column).


def _delta_safe_type(t: pa.DataType) -> pa.DataType:
    """The Delta-storable Arrow type for `t` — `t` itself when already storable.

    Deterministic mapping for the types deltalake rejects:

      time32/time64 → string   "HH:MM:SS[.ffffff]" (see _delta_safe_column)
      duration      → int64    the raw count in the column's own unit
      float16       → float32  exact — every float16 is representable
      null          → string   an all-null column stays all-null
      interval      → string   top-level only; Arrow has no interval→string
                               cast, so _delta_safe_column converts in Python

    Recurses through list/large_list/fixed_size_list/map/struct/dictionary so
    nested occurrences are rewritten too (nested intervals stay unsupported —
    the cast raises, exactly as the Delta write itself would have).
    """
    if pa.types.is_time(t) or pa.types.is_null(t) or pa.types.is_interval(t):
        return pa.string()
    if pa.types.is_duration(t):
        return pa.int64()
    if pa.types.is_float16(t):
        return pa.float32()
    if pa.types.is_list(t):
        return pa.list_(_delta_safe_type(t.value_type))
    if pa.types.is_large_list(t):
        return pa.large_list(_delta_safe_type(t.value_type))
    if pa.types.is_fixed_size_list(t):
        return pa.list_(_delta_safe_type(t.value_type), t.list_size)
    if pa.types.is_map(t):
        return pa.map_(_delta_safe_type(t.key_type), _delta_safe_type(t.item_type))
    if pa.types.is_struct(t):
        return pa.struct([pa.field(f.name, _delta_safe_type(f.type), f.nullable) for f in t])
    if pa.types.is_dictionary(t):
        safe = _delta_safe_type(t.value_type)
        return t if safe.equals(t.value_type) else safe
    return t


def _delta_safe_schema(schema: pa.Schema) -> pa.Schema:
    return pa.schema(
        [pa.field(f.name, _delta_safe_type(f.type), f.nullable) for f in schema],
        metadata=schema.metadata,
    )


def _delta_safe_column(arr):
    """Normalize one column (Array or ChunkedArray) to its Delta-safe type."""
    target = _delta_safe_type(arr.type)
    if target.equals(arr.type):
        return arr
    if pa.types.is_interval(arr.type):
        # No Arrow cast exists for month_day_nano_interval; batches are small
        # enough (DuckDB streams ~100k rows/batch) that a Python loop is fine.
        # ISO-8601-style so the value stays unambiguous: P<months>M<days>DT<secs>S.
        return pa.array(
            [None if v is None else f"P{v.months}M{v.days}DT{v.nanoseconds / 1_000_000_000:g}S"
             for v in arr.to_pylist()],
            type=pa.string(),
        )
    out = arr.cast(target)
    if pa.types.is_time(arr.type):
        # Arrow renders a whole-second time64[us] as "12:34:56.000000"; strip
        # trailing fractional zeros (then a bare dot) so the common case reads
        # as plain HH:MM:SS while sub-second precision is preserved.
        import pyarrow.compute as pc
        out = pc.replace_substring_regex(out, pattern=r"(\.\d*?)0+$", replacement=r"\1")
        out = pc.replace_substring_regex(out, pattern=r"\.$", replacement="")
    return out


def _delta_safe_data(data):
    """Rewrite a Table or RecordBatch so every column is Delta-storable."""
    cols = [_delta_safe_column(data.column(i)) for i in range(data.num_columns)]
    schema = _delta_safe_schema(data.schema)
    if isinstance(data, pa.RecordBatch):
        return pa.RecordBatch.from_arrays(cols, schema=schema)
    return pa.Table.from_arrays(cols, schema=schema)


def _delta_safe_source(source: Union[pa.Table, pa.RecordBatchReader], name: str):
    """The write-boundary normalization merge/overwrite/append all apply.

    Returns `source` unchanged (zero-copy) when its schema is already
    Delta-storable. Otherwise returns a rewritten Table, or — for a
    RecordBatchReader — a wrapping reader that normalizes each batch as it
    streams, so large sources still never materialize in memory.
    """
    target = _delta_safe_schema(source.schema)
    if target.equals(source.schema):
        return source
    changed = ", ".join(
        f"{f.name}: {f.type} → {t.type}"
        for f, t in zip(source.schema, target) if not f.type.equals(t.type)
    )
    print(f"[delta] {name}: normalizing non-Delta column type(s) — {changed}")
    if isinstance(source, pa.RecordBatchReader):
        return pa.RecordBatchReader.from_batches(
            target, (_delta_safe_data(b) for b in source)
        )
    return _delta_safe_data(source)


def _target_row_count(dt: DeltaTable) -> int:
    """Sum num_records from the Delta log's add actions.

    Reads only file-level metadata (parquet footer stats already in the log),
    no data scan. Returns -1 if unavailable so callers can still report.
    """
    try:
        # deltalake ≥1.0 returns an arro3 RecordBatch; bridge to pyarrow.
        batch = pa.record_batch(dt.get_add_actions(flatten=True))
        col = batch.column("num_records")
        return int(sum(v for v in col.to_pylist() if v is not None))
    except Exception:
        return -1


def _log_write_meta(name: str, schema: pa.Schema, row_count: int, mode: str):
    """Print a one-line schema summary for a write. Materialization lineage is
    captured by record_write() into the run record (→ run.json), not here."""
    cols = ', '.join(f.name for f in schema)
    rows_str = f"{row_count:,}" if row_count >= 0 else "?"
    print(f"[{mode}] {name}: {rows_str} rows, {len(schema)} cols ({cols})")


def _source_hash(source, schema: pa.Schema, target_row_count: int) -> str:
    """Hash a merge source.

    For a Table: hash source rowcount + schema (stable across runs when the
    source is unchanged).
    For a RecordBatchReader: the stream has been consumed by deltalake by now,
    so we fall back to target rowcount + schema. This isn't a source-only
    fingerprint but it's still a stable descriptor of the written state.
    """
    import hashlib
    h = hashlib.md5()
    if isinstance(source, pa.Table):
        h.update(f"{len(source)}".encode())
    else:
        h.update(f"{target_row_count}".encode())
    h.update(str(schema).encode())
    return h.hexdigest()[:16]


def _validate_keys(table: pa.Table, keys: list[str], name: str):
    """Validate key columns before merge.

    Checks:
    1. Key columns exist
    2. Key columns have no nulls
    3. Key combination is unique (no duplicates)
    """
    # Check columns exist
    for k in keys:
        if k not in table.column_names:
            raise ValueError(f"[{name}] Key column '{k}' not found. Columns: {table.column_names}")

    # Check for nulls in key columns
    for k in keys:
        null_count = table[k].null_count
        if null_count > 0:
            raise ValueError(f"[{name}] Key column '{k}' has {null_count} nulls. Merge keys cannot be null.")

    # Check uniqueness - group by keys and look for duplicates
    if len(keys) == 1:
        # Single key - use value_counts
        key_col = table[keys[0]]
        unique_count = len(key_col.unique())
        if unique_count != len(table):
            dup_count = len(table) - unique_count
            raise ValueError(
                f"[{name}] Key '{keys[0]}' has {dup_count} duplicate values. "
                f"Merge key must be unique. Check your data or add more columns to key."
            )
    else:
        # Composite key - need to check combination
        import pyarrow.compute as pc

        # Concatenate key columns as strings for uniqueness check
        combined = pc.binary_join_element_wise(
            *[pc.cast(table[k], pa.string()) for k in keys],
            "||"
        )
        unique_count = len(combined.unique())
        if unique_count != len(table):
            dup_count = len(table) - unique_count
            raise ValueError(
                f"[{name}] Key {keys} has {dup_count} duplicate combinations. "
                f"Merge key must be unique. Check your data or add more columns to key."
            )


def merge(
    source: Union[pa.Table, pa.RecordBatchReader],
    name: str,
    *,
    key: Union[str, list[str]],
    partition_by: list[str] = None,
    validate: bool = True
) -> "WriteResult":
    """Upsert data into a Delta table.

    - Inserts new records (key doesn't exist)
    - Updates existing records (key exists)
    - Duplicates impossible

    Args:
        source: PyArrow Table or RecordBatchReader. Readers stream batches
            through deltalake without materializing the full dataset in
            memory — use this for large sources via DuckDB's
            fetch_record_batch() or similar. validate=True is incompatible
            with readers (would consume the stream).
        name: Dataset name
        key: Column(s) that uniquely identify a record
        partition_by: Optional columns to partition by
        validate: Check key uniqueness before merge (default True).
            Must be False for RecordBatchReader sources.

    Returns:
        WriteResult with uri, version, hash, rows.
    """
    source = _delta_safe_source(source, name)
    is_reader = isinstance(source, pa.RecordBatchReader)
    if is_reader and validate:
        raise ValueError(
            "merge(): validate=True cannot be combined with a RecordBatchReader "
            "source — the stream would be consumed by validation. Pass "
            "validate=False or materialize to a pa.Table first."
        )

    if not is_reader and len(source) == 0:
        print(f"[merge] {name}: no data to write")
        return None

    # Normalize key to list
    keys = [key] if isinstance(key, str) else key

    # Validate keys (table-only)
    if validate:
        _validate_keys(source, keys, name)

    schema = source.schema
    column_names = [f.name for f in schema]

    uri = subsets_uri(name)
    opts = backend.deltalake_options(uri)

    # Probe for table existence. If it doesn't exist yet, create it via
    # write_deltalake. Any OTHER exception must propagate — we must NOT
    # silently fall back to overwrite mode because that would destroy an
    # existing table's contents on a transient merge failure.
    try:
        dt = DeltaTable(uri, storage_options=opts)
        table_exists = True
    except Exception as e:
        if not _is_table_not_found(e):
            raise
        table_exists = False

    if not table_exists:
        write_deltalake(
            uri,
            source,
            mode="overwrite",
            partition_by=partition_by,
            storage_options=opts,
            commit_properties=_run_commit_properties(),
        )
        dt = DeltaTable(uri, storage_options=opts)
        new_count = _target_row_count(dt)
        version = dt.version()
        h = _source_hash(source, schema, new_count)
        _log_write_meta(name, schema, new_count, "merge (created)")
    else:
        # Build merge predicate
        predicate = " AND ".join([f"target.{k} = source.{k}" for k in keys])
        updates = {col: f"source.{col}" for col in column_names}

        dt.merge(
            source=source,
            predicate=predicate,
            source_alias="source",
            target_alias="target",
            commit_properties=_run_commit_properties(),
        ).when_matched_update(
            updates=updates
        ).when_not_matched_insert(
            updates=updates
        ).execute()

        # Rowcount from Delta log (parquet footers), not by materializing target.
        # Hash on source rowcount+schema — stable fingerprint for unchanged inputs.
        new_count = _target_row_count(dt)
        version = dt.version()
        h = _source_hash(source, schema, new_count)
        _log_write_meta(name, schema, new_count, f"merge → {new_count:,} total")

    record_write(f"subsets/{name}", version=version, hash=h)
    return WriteResult(uri=uri, version=version, hash=h, rows=new_count)


def overwrite(
    source: Union[pa.Table, pa.RecordBatchReader],
    name: str,
    *,
    partition_by: list[str] = None
) -> "WriteResult":
    """Replace entire Delta table with new data.

    Use for:
    - Snapshots without natural key (current prices, live status)
    - Computed aggregates
    - Data that's fully recomputed each run (e.g. SDMX full-refresh flows
      where the connector pulls the complete dataset on every invocation)

    merge() is preferable only when runs bring PARTIAL data and you want
    target rows not in source to survive — otherwise overwrite is both
    simpler and cheaper (no target-side join).

    Accepts a pa.Table or pa.RecordBatchReader. Readers stream through
    deltalake without materializing the full source in memory — use via
    DuckDB's fetch_record_batch() or similar.
    """
    source = _delta_safe_source(source, name)
    is_reader = isinstance(source, pa.RecordBatchReader)

    if not is_reader and len(source) == 0:
        print(f"[overwrite] {name}: no data to write")
        return None

    schema = source.schema

    uri = subsets_uri(name)
    opts = backend.deltalake_options(uri)

    write_deltalake(
        uri,
        source,
        mode="overwrite",
        partition_by=partition_by,
        storage_options=opts,
        schema_mode="overwrite",
        commit_properties=_run_commit_properties(),
    )

    dt = DeltaTable(uri, storage_options=opts)
    version = dt.version()
    new_count = _target_row_count(dt)
    h = _source_hash(source, schema, new_count)

    _log_write_meta(name, schema, new_count, "overwrite")
    record_write(f"subsets/{name}", version=version, hash=h)
    return WriteResult(uri=uri, version=version, hash=h, rows=new_count)


def append(
    source: Union[pa.Table, pa.RecordBatchReader],
    name: str,
    *,
    partition_by: list[str] = None
) -> "WriteResult":
    """Append data to a Delta table.

    WARNING: No deduplication! Use ONLY for:
    - Immutable events (audit logs, raw API responses)
    - Data where duplicates are impossible by design
    - Chunked loads into an already-partitioned table where each chunk's
      partition keys are disjoint from previously-written chunks

    Always use partition_by for cleanup capability.

    Accepts pa.Table or pa.RecordBatchReader. Readers stream through
    deltalake without materializing in memory — use for chunked loads
    (e.g. per-partition dedup) driven by DuckDB's fetch_record_batch().
    """
    source = _delta_safe_source(source, name)
    is_reader = isinstance(source, pa.RecordBatchReader)

    if not is_reader and len(source) == 0:
        print(f"[append] {name}: no data to write")
        return None

    if partition_by is None:
        print(f"⚠️  Warning: append() without partition_by makes cleanup difficult")

    schema = source.schema

    uri = subsets_uri(name)
    opts = backend.deltalake_options(uri)

    write_deltalake(
        uri,
        source,
        mode="append",
        partition_by=partition_by,
        storage_options=opts,
        schema_mode="merge",  # Allow schema evolution for append
        commit_properties=_run_commit_properties(),
    )

    dt = DeltaTable(uri, storage_options=opts)
    version = dt.version()
    new_count = _target_row_count(dt)
    h = _source_hash(source, schema, new_count)

    _log_write_meta(name, schema, new_count, "append")
    record_write(f"subsets/{name}", version=version, hash=h)
    return WriteResult(uri=uri, version=version, hash=h, rows=new_count)
