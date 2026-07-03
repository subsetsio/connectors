"""Runtime executor for SqlNodeSpec: raw asset(s) in → SQL → one Delta table.

The orchestrator routes SqlNodeSpec nodes here instead of calling a
connector-authored fn. `run_sql_node` is a top-level function so it survives
spawn-context pickling; the spec instance itself (id, deps, sql) is the only
payload.

Per dep, the raw file set is resolved through the connector's RAW MANIFEST
(see raw_manifest.py): the manifest's fragment paths may span multiple run
dirs, so a dep whose fetch was maintain-skipped this run still resolves to
the objects a prior run committed. When the manifest has no entry for the dep
(pre-manifest connectors), resolution falls back to globbing the run-scoped
raw dir (`<dep>.<ext>` first, then the batch layout `<dep>-*`). Either way,
files are mapped to the matching DuckDB reader by extension and registered as
a temp view named after the dep id. The connector's SQL then runs against
those views and the result streams into `overwrite(<table>)`. Zero rows is a
failure: the transform is the correctness gate on raw, and an empty publish
means the raw shape or the SQL is wrong.
"""

from __future__ import annotations

import duckdb

from . import raw_manifest
from .config import raw_uri
from .delta import overwrite
from .duckdb import _configure
from .spec import SqlNodeSpec

# Extension (after stripping compression suffixes) → DuckDB table function.
# DuckDB infers compression from the .zst/.gz suffix itself, so the reader
# gets the full path; we only strip suffixes to decide WHICH reader.
_COMPRESSION_SUFFIXES = (".zst", ".gz", ".bz2", ".xz")
_READERS = {
    ".parquet": "read_parquet",
    ".ndjson": "read_json_auto",
    ".jsonl": "read_json_auto",
    ".json": "read_json_auto",
    ".csv": "read_csv_auto",
    ".tsv": "read_csv_auto",
}


def _reader_for(rel_path: str) -> str | None:
    """Map a raw file's name to its DuckDB reader, or None if unreadable."""
    name = rel_path.lower()
    for suffix in _COMPRESSION_SUFFIXES:
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break
    for ext, reader in _READERS.items():
        if name.endswith(ext):
            return reader
    return None


def _raw_base_uri() -> str:
    """The run-scoped raw dir (s3:// or local), derived by probing raw_uri
    (the "__probe__" asset is never created — raw_uri only builds the path)."""
    return raw_uri("__probe__", "__").rsplit("/", 1)[0]


def _glob_raw(pattern: str) -> list[str]:
    """Glob the run-scoped raw dir — the PRE-MANIFEST read fallback only
    (manifest-first resolution lives in `_read_clause`)."""
    from .io import list_raw_files
    return list_raw_files(pattern)


def _read_clause(dep_id: str) -> tuple[list[str], str]:
    """Build the DuckDB FROM-clause for one dep's raw file(s).
    Returns (raw path refs, FROM-clause) so the caller can record reads.

    Manifest first: the committed raw manifest's fragment paths for this dep
    (exact asset key, else the flat `<dep>-*` batch/fragment assets) — these
    may point into multiple run dirs. Glob fallback only when the manifest
    knows nothing: exact-name match (`<dep>.<ext>`) wins; only when absent do
    we accept the batch layout (`<dep>-*`) so a sibling asset whose id extends
    this one (e.g. `slug-us` vs `slug-us-east`) can't be swallowed by the glob.
    """
    resolved = raw_manifest.dep_fragments(dep_id)
    if resolved is not None:
        rels = [ref for ref, _ in resolved]
        paths = [uri for _, uri in resolved]
        source = "manifest"
    else:
        rels = _glob_raw(f"{dep_id}.*")
        if not rels:
            rels = _glob_raw(f"{dep_id}-*")
        if not rels:
            raise FileNotFoundError(
                f"SqlNodeSpec dep {dep_id!r}: no raw files found "
                f"(no manifest entry; globbed '{dep_id}.*' and '{dep_id}-*')"
            )
        base = _raw_base_uri()
        paths = [f"{base}/{rel}" for rel in rels]
        source = "glob"

    readers = {r for r in (_reader_for(rel) for rel in rels) if r}
    unreadable = [rel for rel in rels if _reader_for(rel) is None]
    if unreadable:
        raise ValueError(
            f"SqlNodeSpec dep {dep_id!r}: raw file(s) not SQL-readable "
            f"{unreadable[:5]} (via {source}) — downloads feeding a SQL "
            "transform must write parquet/ndjson/csv (compressed ok); "
            "normalize in the download fn"
        )
    if len(readers) > 1:
        raise ValueError(
            f"SqlNodeSpec dep {dep_id!r}: mixed raw formats {sorted(readers)} "
            f"across {len(rels)} files (via {source}) — one format per asset"
        )

    return rels, f"{readers.pop()}({paths})"


def _canonical_type(type_expr: str) -> str:
    """Canonicalize a declared DuckDB type through DuckDB itself, so contract
    aliases (TEXT, FLOAT8, INT64, STRING) compare equal to the binder's
    spelling (VARCHAR, DOUBLE, BIGINT)."""
    return str(duckdb.sql(f"SELECT CAST(NULL AS {type_expr}) AS c").types[0])


def _verify_contract(spec: SqlNodeSpec) -> "duckdb.DuckDBPyRelation":
    """Bind the query and verify its output against spec.columns (verify-only).

    Runs BEFORE execution: DuckDB's binder resolves names and types without
    scanning the data, so a contract breach costs nothing and never touches
    the existing Delta table. The check is strict — exact names, exact order,
    exact (canonicalized) types. The SQL must cast; the runtime never coerces.
    Returns the bound relation so the caller executes the same plan it checked.
    """
    rel = duckdb.sql(spec.sql)
    if spec.columns is None:
        return rel

    actual = list(zip(rel.columns, [str(t) for t in rel.types]))
    expected = [(c.name, _canonical_type(c.type)) for c in spec.columns]

    if actual == expected:
        return rel

    lines = [f"SqlNodeSpec {spec.id!r}: output does not match contract"]
    width = max(len(expected), len(actual))
    for i in range(width):
        exp = expected[i] if i < len(expected) else None
        act = actual[i] if i < len(actual) else None
        if exp == act:
            continue
        exp_s = f"{exp[0]} {exp[1]}" if exp else "(nothing — extra output column)"
        act_s = f"{act[0]} {act[1]}" if act else "(nothing — missing from output)"
        lines.append(f"  [{i}] contract: {exp_s:<40} output: {act_s}")
    lines.append("  Fix the SQL (names, order, casts) or update the contract — "
                 "the runtime never coerces.")
    raise ValueError("\n".join(lines))


def run_sql_node(spec: SqlNodeSpec) -> None:
    """Execute one SqlNodeSpec: views for deps, run sql, overwrite Delta table."""
    _configure()  # S3 credentials for DuckDB when in cloud mode

    from .tracking import record_read

    for dep in spec.deps:
        rels, clause = _read_clause(dep)
        duckdb.sql(f'CREATE OR REPLACE TEMP VIEW "{dep}" AS SELECT * FROM {clause}')
        # DuckDB reads bypass load_raw_* so lineage is recorded here. Manifest
        # refs already carry a raw/ segment (they may span run dirs); glob rels
        # are relative to this run's raw dir and get the historic raw/ prefix.
        for rel in rels:
            record_read(rel if (rel.startswith("raw/") or "/raw/" in rel) else f"raw/{rel}")
        print(f'[sql-transform] view "{dep}" <- {clause[:200]}')

    # Verify-only contract check at bind time — a breach fails the node before
    # a single row is read or the existing table is touched.
    rel = _verify_contract(spec)
    if spec.columns is not None:
        print(f"[sql-transform] contract ok: {len(spec.columns)} column(s)")

    # fetch_record_batch() streams — the result never fully materializes in
    # memory. Peek until the first non-empty batch BEFORE writing: an empty
    # result must fail without touching (and possibly clobbering) an existing
    # good table.
    reader = rel.fetch_record_batch()
    peeked = []
    for batch in reader:
        peeked.append(batch)
        if batch.num_rows:
            break
    if not any(b.num_rows for b in peeked):
        raise ValueError(
            f"SqlNodeSpec {spec.id!r}: query produced 0 rows — transform is the "
            "correctness gate, an empty publish means raw or SQL is wrong"
        )

    def _chain():
        yield from peeked
        yield from reader

    import pyarrow as pa
    overwrite(pa.RecordBatchReader.from_batches(reader.schema, _chain()), spec.table)
