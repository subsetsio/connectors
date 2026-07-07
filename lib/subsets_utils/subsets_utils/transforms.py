"""File-based transform authoring: transforms/<table>.sql + <table>.yml.

The authoring format for explicit SQL transforms. Each published table is a
pair of files in the connector's `src/transforms/` directory:

    transforms/
      cbs-70072ned.sql    # the transform: one DuckDB SELECT, explicit casts
      cbs-70072ned.yml    # the contract: columns/types/descriptions, key, temporal

The filename stem IS the published table name; the node id is `<stem>-transform`
and `deps` defaults to `[<stem>]` (the 1:1 raw asset). The loader parses both
files into a SqlNodeSpec — the same validated unit the runtime executes for
Python-authored transforms — so orchestration, DAG_TARGET filtering, and
resume behavior are identical regardless of where a transform was authored.

yml schema (unknown keys are errors — typo safety):

    deps: [asset-id, ...]     # optional; default [<stem>]
    key: [col, ...]           # optional; [] = explicitly keyless; absent = undeclared
    temporal: period          # optional; must be a contract column
    write_mode: overwrite     # optional; overwrite (default) | merge | append.
                              # merge upserts on `key` (requires non-empty key) —
                              # use when runs bring partial/incremental data so
                              # the table isn't fully replaced every run.
    sort: [col, ...]          # optional; physical row order of the published
                              # table (ascending, nulls last). Deterministic
                              # output + range-skip stats; temporal first, then
                              # key tiebreakers. Absent = unsorted.
    columns:                  # required, non-empty, ordered
      - name: period          # published column name
        type: VARCHAR         # DuckDB type (aliases fine — canonicalized at verify)
        description: ...      # optional

The contract is verify-only: sql_transform binds the query and fails the node
when the output's names/order/types don't match `columns` exactly. The SQL
must do its own casting — the runtime never coerces.

Loaded by orchestrator.load_nodes() from `src/transforms/` alongside the
`src/nodes/` module scan. A file-based spec whose id collides with a
Python-authored spec REPLACES it — this is the migration path for catalog
connectors: drop in an explicit file and it overrides the generic
comprehension entry for that table, no Python edit needed.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from .spec import ColumnSpec, SqlNodeSpec

_YML_KEYS = {"deps", "key", "temporal", "write_mode", "sort", "columns"}
_COLUMN_KEYS = {"name", "type", "description"}


def _fail(path: Path, msg: str) -> ValueError:
    return ValueError(f"{path}: {msg}")


def _parse_columns(path: Path, raw_columns) -> tuple[ColumnSpec, ...]:
    if not isinstance(raw_columns, list) or not raw_columns:
        raise _fail(path, "`columns` must be a non-empty list")
    cols = []
    for i, entry in enumerate(raw_columns):
        if not isinstance(entry, dict):
            raise _fail(path, f"columns[{i}] must be a mapping (got {type(entry).__name__})")
        unknown = set(entry) - _COLUMN_KEYS
        if unknown:
            raise _fail(path, f"columns[{i}] has unknown key(s) {sorted(unknown)} "
                              f"(allowed: {sorted(_COLUMN_KEYS)})")
        if "name" not in entry or "type" not in entry:
            raise _fail(path, f"columns[{i}] needs `name` and `type`")
        try:
            cols.append(ColumnSpec(
                name=str(entry["name"]),
                type=str(entry["type"]),
                description=(str(entry["description"]) if entry.get("description") is not None else None),
            ))
        except (TypeError, ValueError) as e:
            raise _fail(path, f"columns[{i}]: {e}") from e
    return tuple(cols)


def _load_pair(sql_path: Path, yml_path: Path) -> SqlNodeSpec:
    table = sql_path.stem

    sql = sql_path.read_text()
    if not sql.strip():
        raise _fail(sql_path, "empty SQL file")

    try:
        doc = yaml.safe_load(yml_path.read_text())
    except yaml.YAMLError as e:
        raise _fail(yml_path, f"invalid YAML: {e}") from e
    if not isinstance(doc, dict):
        raise _fail(yml_path, f"top level must be a mapping (got {type(doc).__name__})")

    unknown = set(doc) - _YML_KEYS
    if unknown:
        raise _fail(yml_path, f"unknown key(s) {sorted(unknown)} (allowed: {sorted(_YML_KEYS)})")
    if "columns" not in doc:
        raise _fail(yml_path, "missing required `columns` — the contract is the point of the file")

    deps = doc.get("deps", [table])
    if isinstance(deps, str) or not isinstance(deps, list) or not all(isinstance(d, str) for d in deps):
        raise _fail(yml_path, "`deps` must be a list of asset-id strings")

    # key: absent → None (undeclared); [] → () (explicitly keyless); list → tuple.
    key = doc.get("key", None)
    if key is not None:
        if isinstance(key, str) or not isinstance(key, list) or not all(isinstance(k, str) for k in key):
            raise _fail(yml_path, "`key` must be a list of column-name strings ([] = keyless)")
        key = tuple(key)

    temporal = doc.get("temporal", None)
    if temporal is not None and not isinstance(temporal, str):
        raise _fail(yml_path, "`temporal` must be a column-name string")

    write_mode = doc.get("write_mode", "overwrite")
    if not isinstance(write_mode, str):
        raise _fail(yml_path, "`write_mode` must be a string: overwrite | merge | append")

    sort = doc.get("sort", None)
    if sort is not None:
        if isinstance(sort, str) or not isinstance(sort, list) or not all(isinstance(c, str) for c in sort):
            raise _fail(yml_path, "`sort` must be a list of column-name strings")
        sort = tuple(sort)

    try:
        return SqlNodeSpec(
            id=f"{table}-transform",
            deps=deps,
            sql=sql,
            key=key,
            temporal=temporal,
            columns=_parse_columns(yml_path, doc["columns"]),
            write_mode=write_mode,
            sort=sort,
        )
    except (TypeError, ValueError) as e:
        raise _fail(yml_path, str(e)) from e


def load_transform_dir(transforms_dir: Path | str) -> list[SqlNodeSpec]:
    """Load every <table>.sql + <table>.yml pair in `transforms_dir`.

    An unpaired .sql or .yml is an error, not a skip — a half-authored
    transform must never silently drop a table from the DAG. Files starting
    with `_` are ignored (scratch/templates). Returns specs sorted by id.
    """
    transforms_dir = Path(transforms_dir)
    if not transforms_dir.exists():
        return []

    sql_files = {p.stem: p for p in transforms_dir.glob("*.sql") if not p.name.startswith("_")}
    yml_files = {p.stem: p for p in transforms_dir.glob("*.yml") if not p.name.startswith("_")}
    yml_files.update({p.stem: p for p in transforms_dir.glob("*.yaml") if not p.name.startswith("_")})

    missing_yml = sorted(set(sql_files) - set(yml_files))
    missing_sql = sorted(set(yml_files) - set(sql_files))
    if missing_yml:
        raise ValueError(f"{transforms_dir}: .sql without contract .yml: {missing_yml}")
    if missing_sql:
        raise ValueError(f"{transforms_dir}: contract .yml without .sql: {missing_sql}")

    return [_load_pair(sql_files[stem], yml_files[stem]) for stem in sorted(sql_files)]
