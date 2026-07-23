"""Post-publish table audit: checks/<table>.yml in → one aggregate scan of the
published Delta table → invariant verdicts + a run-over-run regression compare.

The publish-side counterpart of the download-stage test engine. Each published
table may carry a `checks/<table>.yml` (compiled by `hardened compile-checks`
from the settled model + the transform contract, hand-editable afterwards).
The loader synthesizes a CheckNodeSpec per file — id `<table>-checks`,
depending on `<table>-transform` — so the audit runs strictly AFTER the
publish. Detection, never prevention: a `block` violation fails the check
node (the run concludes `done_with_failures` under `dag_on_failure:
continue`, which operate already classifies as degraded); the published
write is not rolled back.

yml schema (unknown keys are errors — typo safety, same as transforms.py):

    key: [country, year]        # audited grain (published names) — regression stat
    temporal: year              # audited time axis — regression stat
    checks:                     # invariants, evaluated in ONE aggregate scan
      - kind: unique            #   unique | not_null | enum | row_floor
        columns: [country, year]
      - kind: not_null
        col: country
      - kind: row_floor
        min: 612
      - kind: not_null          # severity: warn records without failing —
        col: value              # for observed-but-never-authored facts
        severity: warn
    regression:                 # run-over-run compare vs the persisted baseline
      row_shrink_tolerance: 0.10
      key_shrink_tolerance: 0.10
      temporal_monotonic: true

The regression baseline (row count, exact key cardinality, temporal max,
table version) lives in the check node's own state (`load_state`/`save_state`
— R2 in cloud, so production runs on any runner share it). The baseline only
advances past a run whose regression compare held: a broken shrink keeps
alarming every run until the data recovers or the new shape is explicitly
accepted (recompile the checks, or one run with
`SUBSETS_RESET_CHECK_BASELINE=1`, which skips the compare and re-records
the baseline from the current scan).

`SUBSETS_SKIP_CHECKS=1` bypasses every audit (emergency valve, mirrors
`FORCE_REFRESH` / `SUBSETS_FORCE_WRITE`).
"""

from __future__ import annotations

import os
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

from .spec import CheckNodeSpec, CheckSpec, RegressionSpec

_YML_KEYS = {"key", "temporal", "checks", "regression"}
_CHECK_ENTRY_KEYS = {"kind", "severity", "columns", "col", "values", "min"}
_REGRESSION_KEYS = {"row_shrink_tolerance", "key_shrink_tolerance", "temporal_monotonic"}

STATE_KEY = "table_stats"
_TRANSFORM_SUFFIX = "-transform"
_CHECKS_SUFFIX = "-checks"


# =============================================================================
# Loading
# =============================================================================


def _fail(path: Path, msg: str) -> ValueError:
    return ValueError(f"{path}: {msg}")


def _parse_check(path: Path, i: int, entry) -> CheckSpec:
    if not isinstance(entry, dict):
        raise _fail(path, f"checks[{i}] must be a mapping (got {type(entry).__name__})")
    unknown = set(entry) - _CHECK_ENTRY_KEYS
    if unknown:
        raise _fail(path, f"checks[{i}] has unknown key(s) {sorted(unknown)} "
                          f"(allowed: {sorted(_CHECK_ENTRY_KEYS)})")
    if "kind" not in entry:
        raise _fail(path, f"checks[{i}] needs `kind`")
    columns = entry.get("columns", [])
    if isinstance(columns, str) or not isinstance(columns, list):
        raise _fail(path, f"checks[{i}]: `columns` must be a list of column names")
    values = entry.get("values", [])
    if isinstance(values, str) or not isinstance(values, list):
        raise _fail(path, f"checks[{i}]: `values` must be a list of strings")
    try:
        return CheckSpec(
            kind=str(entry["kind"]),
            severity=str(entry.get("severity", "block")),
            columns=tuple(columns),
            col=entry.get("col"),
            values=tuple(values),
            min=entry.get("min"),
        )
    except (TypeError, ValueError) as e:
        raise _fail(path, f"checks[{i}]: {e}") from e


def _parse_regression(path: Path, raw) -> RegressionSpec:
    if not isinstance(raw, dict):
        raise _fail(path, f"`regression` must be a mapping (got {type(raw).__name__})")
    unknown = set(raw) - _REGRESSION_KEYS
    if unknown:
        raise _fail(path, f"regression has unknown key(s) {sorted(unknown)} "
                          f"(allowed: {sorted(_REGRESSION_KEYS)})")
    mono = raw.get("temporal_monotonic", False)
    if not isinstance(mono, bool):
        raise _fail(path, "regression.temporal_monotonic must be a boolean")
    try:
        return RegressionSpec(
            row_shrink_tolerance=raw.get("row_shrink_tolerance"),
            key_shrink_tolerance=raw.get("key_shrink_tolerance"),
            temporal_monotonic=mono,
        )
    except (TypeError, ValueError) as e:
        raise _fail(path, str(e)) from e


def _load_file(path: Path) -> CheckNodeSpec:
    table = path.stem
    try:
        doc = yaml.safe_load(path.read_text())
    except yaml.YAMLError as e:
        raise _fail(path, f"invalid YAML: {e}") from e
    if not isinstance(doc, dict):
        raise _fail(path, f"top level must be a mapping (got {type(doc).__name__})")

    unknown = set(doc) - _YML_KEYS
    if unknown:
        raise _fail(path, f"unknown key(s) {sorted(unknown)} (allowed: {sorted(_YML_KEYS)})")

    key = doc.get("key", [])
    if isinstance(key, str) or not isinstance(key, list) or not all(isinstance(k, str) for k in key):
        raise _fail(path, "`key` must be a list of column-name strings")

    temporal = doc.get("temporal")
    if temporal is not None and not isinstance(temporal, str):
        raise _fail(path, "`temporal` must be a column-name string")

    raw_checks = doc.get("checks", [])
    if not isinstance(raw_checks, list):
        raise _fail(path, "`checks` must be a list")
    checks = tuple(_parse_check(path, i, e) for i, e in enumerate(raw_checks))

    regression = None
    if doc.get("regression") is not None:
        regression = _parse_regression(path, doc["regression"])

    try:
        return CheckNodeSpec(
            id=f"{table}{_CHECKS_SUFFIX}",
            deps=(f"{table}{_TRANSFORM_SUFFIX}",),
            table=table,
            key=tuple(key),
            temporal=temporal,
            checks=checks,
            regression=regression,
        )
    except (TypeError, ValueError) as e:
        raise _fail(path, str(e)) from e


def load_checks_dir(checks_dir: Path | str) -> list[CheckNodeSpec]:
    """Load every `<table>.yml` in `checks_dir` into a CheckNodeSpec.

    A malformed file is an error, not a skip — a half-authored audit must
    never silently drop coverage. Files starting with `_` are ignored
    (scratch/templates). Returns specs sorted by id."""
    checks_dir = Path(checks_dir)
    if not checks_dir.exists():
        return []
    files = sorted(
        p for pat in ("*.yml", "*.yaml") for p in checks_dir.glob(pat)
        if not p.name.startswith("_")
    )
    return [_load_file(p) for p in files]


# =============================================================================
# Execution
# =============================================================================


def _quote(col: str) -> str:
    return '"' + col.replace('"', '""') + '"'


def _sql_lit(v: str) -> str:
    return "'" + v.replace("'", "''") + "'"


def _jsonsafe(v):
    if isinstance(v, (datetime, date)):
        return v.isoformat()
    if isinstance(v, (int, float, str, bool)) or v is None:
        return v
    return str(v)


def _build_query(spec: CheckNodeSpec, view: str) -> tuple[str, dict[str, str]]:
    """ONE aggregate SELECT over the published table: row count, exact key
    cardinality, temporal max, plus every check's statistic. Returns
    (sql, alias->semantic name)."""
    sel = ["count(*) AS s_rows"]
    if spec.key:
        tup = ", ".join(_quote(c) for c in spec.key)
        sel.append(f"count(DISTINCT ({tup})) AS s_key_distinct")
    if spec.temporal:
        sel.append(f"max({_quote(spec.temporal)}) AS s_temporal_max")
    for i, c in enumerate(spec.checks):
        if c.kind == "unique":
            tup = ", ".join(_quote(col) for col in c.columns)
            sel.append(f"count(*) - count(DISTINCT ({tup})) AS c{i}")
        elif c.kind == "not_null":
            sel.append(f"count(*) FILTER (WHERE {_quote(c.col)} IS NULL) AS c{i}")
        elif c.kind == "enum":
            vals = ", ".join(_sql_lit(v) for v in c.values)
            cc = _quote(c.col)
            sel.append(f"count(*) FILTER (WHERE {cc} IS NOT NULL AND "
                       f"CAST({cc} AS VARCHAR) NOT IN ({vals})) AS c{i}")
        elif c.kind == "row_floor":
            pass  # uses s_rows
    return f"SELECT {', '.join(sel)} FROM {view}", {}


def _evaluate(spec: CheckNodeSpec, row: dict) -> list[dict]:
    """Expected-vs-observed for every invariant check."""
    n = row["s_rows"]
    out = []
    for i, c in enumerate(spec.checks):
        rec = {"kind": c.kind, "severity": c.severity}
        if c.kind == "unique":
            obs = row[f"c{i}"]
            rec.update(col=list(c.columns), expected="0 duplicate rows",
                       observed=f"{obs} duplicates", passed=(obs == 0))
        elif c.kind == "not_null":
            obs = row[f"c{i}"]
            rec.update(col=c.col, expected="0 nulls",
                       observed=f"{obs} nulls", passed=(obs == 0))
        elif c.kind == "enum":
            obs = row[f"c{i}"]
            rec.update(col=c.col, expected=f"in {list(c.values)}",
                       observed=f"{obs} outside", passed=(obs == 0))
        elif c.kind == "row_floor":
            rec.update(col=None, expected=f">= {c.min} rows",
                       observed=n, passed=(n >= c.min))
        out.append(rec)
    return out


def _comparable(prev, cur):
    """Both values, coerced to a comparable pair, or None when the stored
    baseline and the current scan don't share a type (schema changed — the
    baseline resets rather than false-alarms)."""
    if prev is None or cur is None:
        return None
    if isinstance(prev, bool) or isinstance(cur, bool):
        return None
    if isinstance(prev, (int, float)) and isinstance(cur, (int, float)):
        return prev, cur
    if isinstance(prev, str) and isinstance(cur, str):
        return prev, cur
    return None


def _evaluate_regression(spec: CheckNodeSpec, stats: dict, prev: dict | None) -> list[dict]:
    """Current scan vs the persisted baseline. No baseline → one informational
    record and every comparison passes (the baseline is recorded this run)."""
    r = spec.regression
    if r is None:
        return []
    if not isinstance(prev, dict) or "row_count" not in prev:
        return [{"kind": "baseline", "severity": "block", "passed": True,
                 "expected": "previous run stats", "observed": "none — baseline recorded this run"}]

    out = []
    if r.row_shrink_tolerance is not None and isinstance(prev.get("row_count"), int):
        floor_n = int(prev["row_count"] * (1.0 - r.row_shrink_tolerance))
        obs = stats["row_count"]
        out.append({"kind": "row_shrink", "severity": "block",
                    "expected": f">= {floor_n} rows (prev {prev['row_count']}, "
                                f"tolerance {r.row_shrink_tolerance})",
                    "observed": obs, "passed": obs >= floor_n})
    if (r.key_shrink_tolerance is not None and spec.key
            and isinstance(prev.get("key_distinct"), int)):
        floor_k = int(prev["key_distinct"] * (1.0 - r.key_shrink_tolerance))
        obs = stats.get("key_distinct")
        out.append({"kind": "key_shrink", "severity": "block",
                    "expected": f">= {floor_k} distinct keys (prev {prev['key_distinct']}, "
                                f"tolerance {r.key_shrink_tolerance})",
                    "observed": obs, "passed": obs is not None and obs >= floor_k})
    if r.temporal_monotonic and spec.temporal:
        pair = _comparable(prev.get("temporal_max"), stats.get("temporal_max"))
        if pair is None:
            out.append({"kind": "temporal_monotonic", "severity": "block", "passed": True,
                        "expected": f"max({spec.temporal}) comparable to baseline",
                        "observed": f"incomparable (prev {prev.get('temporal_max')!r}, "
                                    f"now {stats.get('temporal_max')!r}) — baseline resets"})
        else:
            p, c = pair
            out.append({"kind": "temporal_monotonic", "severity": "block",
                        "expected": f"max({spec.temporal}) >= {p!r} (baseline)",
                        "observed": c, "passed": c >= p})
    return out


def _render(rec: dict) -> str:
    mark = "ok " if rec.get("passed") else ("WARN" if rec.get("severity") == "warn" else "FAIL")
    col = rec.get("col")
    col_s = f" {col}" if col else ""
    return (f"  [{mark}] {rec['kind']}{col_s}: expected {rec.get('expected')}, "
            f"observed {rec.get('observed')}")


def run_check_node(spec: CheckNodeSpec) -> None:
    """Execute one CheckNodeSpec: scan the published Delta table once,
    evaluate invariants + regression vs the persisted baseline, advance the
    baseline, and raise on any `block` violation."""
    if os.environ.get("SUBSETS_SKIP_CHECKS") == "1":
        print(f"[checks] {spec.table}: SUBSETS_SKIP_CHECKS=1 — audit skipped")
        return

    import duckdb
    from deltalake import DeltaTable

    from .config import subsets_uri
    from .io import load_state, save_state
    from .storage import backend

    uri = subsets_uri(spec.table)
    opts = backend.deltalake_options(uri)
    # The dep on <table>-transform means the publish already happened; a
    # missing table here is a real failure, never a skip.
    dt = DeltaTable(uri, storage_options=opts)
    version = dt.version()

    con = duckdb.connect()
    con.register("__checks_t", dt.to_pyarrow_dataset())
    sql, _ = _build_query(spec, "__checks_t")
    cur = con.execute(sql)
    names = [d[0] for d in cur.description]
    row = dict(zip(names, cur.fetchone()))
    con.close()

    stats = {
        "row_count": int(row["s_rows"]),
        "key_distinct": int(row["s_key_distinct"]) if spec.key else None,
        "temporal_max": _jsonsafe(row.get("s_temporal_max")) if spec.temporal else None,
        "version": version,
        "run_id": os.environ.get("RUN_ID", "unknown"),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }

    state = load_state(spec.id)
    prev = state.get(STATE_KEY)
    reset = os.environ.get("SUBSETS_RESET_CHECK_BASELINE") == "1"
    if reset:
        print(f"[checks] {spec.table}: SUBSETS_RESET_CHECK_BASELINE=1 — "
              "regression compare skipped, baseline re-recorded from this scan")
    results = _evaluate(spec, row)
    regression = [] if reset else _evaluate_regression(spec, stats, prev)
    results += regression

    print(f"[checks] {spec.table}: v{version}, {stats['row_count']} rows"
          + (f", {stats['key_distinct']} distinct keys" if spec.key else "")
          + (f", max({spec.temporal})={stats['temporal_max']}" if spec.temporal else ""))
    for rec in results:
        print(_render(rec))

    blocking = [r for r in results if not r.get("passed") and r.get("severity") == "block"]
    warns = [r for r in results if not r.get("passed") and r.get("severity") == "warn"]

    # The baseline only advances past a run whose REGRESSION compare held (or
    # was explicitly reset). Advancing it on a violation would make a broken
    # shrink read healthy one run later — the alarm must repeat until the data
    # recovers or a human/agent accepts the new shape (recompile the checks,
    # or one run with SUBSETS_RESET_CHECK_BASELINE=1). Invariant (non-
    # regression) failures don't hold the baseline back: they judge current
    # content, not the run-over-run trajectory.
    regression_broken = any(not r.get("passed") and r.get("severity") == "block"
                            for r in regression)
    if not regression_broken:
        state[STATE_KEY] = stats
    state["last_check"] = {
        "run_id": stats["run_id"],
        "checked_at": stats["recorded_at"],
        "version": version,
        "violations": blocking,
        "warns": warns,
    }
    if not blocking:
        # A clean audit records its fingerprint so an identical future
        # invocation (same table state, same check spec) skips in the parent.
        # A blocking violation records nothing — the audit repeats until the
        # data recovers or the checks are recompiled.
        from .transform_state import record_check
        state = record_check(spec, state)
    save_state(spec.id, state)

    if blocking:
        lines = [f"{spec.table}: {len(blocking)} blocking check violation(s) "
                 f"(published v{version} is suspect — investigate before the next publish):"]
        lines += [_render(r) for r in blocking]
        raise ValueError("\n".join(lines))
