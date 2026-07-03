"""Raw asset profiler: a context-efficient structural digest of raw, for
authoring explicit transforms and contracts.

The profile is computed through the SAME read path the transform runtime uses
(sql_transform._read_clause → read_parquet / read_json_auto / read_csv_auto),
so what it reports is by construction what the transform's SQL will see —
same manifest/glob resolution, same reader, same type inference. Output is
sized to structural complexity, not file size: a 100M-row asset and a 1k-row
one cost about the same to read as a profile.

Profiles are EPHEMERAL: regenerated on demand from raw, never committed.
The committed artifact is the curated transforms/<table>.sql + .yml pair;
--draft-dir writes ready-to-curate skeletons of both.

Usage (from a connector directory, local mode):

    python -m subsets_utils.profile <asset-id> [...]
        [--sample N]      profiling-query row cap (default 1_000_000; row
                          count and fragment checks always see everything)
        [--full]          no sampling
        [--draft-dir D]   also write D/<asset>.sql + D/<asset>.yml drafts
        [--out FILE]      write the JSON profile(s) to FILE instead of stdout

Output blocks per asset:
    treatment — how it was read: reader, files, sizes, sampling
    envelope  — row count, column count, nested columns
    columns   — per column: type, null %, uniqueness, range, samples,
                quality flags (numbers-as-strings, null-like strings,
                whitespace, constant, temporal patterns + mixed granularity)
    alerts    — fragment schema drift, wide tables, nested structures,
                zero rows, unreadable/mixed formats
    draft     — suggested contract (published names, types, temporal/key
                candidates) that --draft-dir materializes as files

A profile never raises: any failure returns an error profile with the
exception attached, so a fleet-wide sweep completes and reports.
"""

from __future__ import annotations

import argparse
import json
import re
import sys

import duckdb

from .duckdb import _configure
from .sql_transform import _read_clause, _reader_for

SAMPLE_DEFAULT = 1_000_000
MAX_SAMPLE_VALUES = 5
MAX_VALUE_CHARS = 80
MAX_FRAGMENT_DESCRIBES = 25
WIDE_TABLE_ALERT = 250

# Patterns for temporal-candidate detection on VARCHAR columns. Ordered by
# granularity; names feed the mixed-granularity check and the draft's
# suggested casts.
_TEMPORAL_PATTERNS = {
    "year": r"^(1[6-9]|20)\d{2}$",
    "year_month": r"^\d{4}-(0[1-9]|1[0-2])$",
    "date": r"^\d{4}-\d{2}-\d{2}$",
    "timestamp": r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}",
    "quarter": r"^\d{4}-?Q[1-4]$",
}
_NUMERIC_RE = r"^[+-]?\d+([.,]\d+)?([eE][+-]?\d+)?$"
_INTEGER_RE = r"^[+-]?\d+$"
_NULL_LIKE = ("", "n/a", "na", "null", "none", "-", ".", "nan", "nil", "(leeg)", "..")

_TEMPORAL_DUCK_TYPES = ("DATE", "TIMESTAMP", "TIMESTAMP WITH TIME ZONE", "TIME")


def _q(identifier: str) -> str:
    """Quote a SQL identifier (double any embedded double-quotes)."""
    return '"' + identifier.replace('"', '""') + '"'


def _lit(value: str) -> str:
    """Quote a SQL string literal."""
    return "'" + value.replace("'", "''") + "'"


def _fmt_value(v):
    """JSON-safe, truncated rendering of a sampled/aggregated value."""
    if v is None:
        return None
    if isinstance(v, bool):
        return v
    if isinstance(v, float):
        return round(v, 6)
    if isinstance(v, int):
        return v
    s = str(v)
    return s if len(s) <= MAX_VALUE_CHARS else s[:MAX_VALUE_CHARS] + "…"


def _rows_as_dicts(rel) -> list[dict]:
    cols = rel.columns
    return [dict(zip(cols, row)) for row in rel.fetchall()]


def _snake_case(name: str) -> str:
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name.strip())
    s = re.sub(r"[^0-9a-zA-Z]+", "_", s).strip("_").lower()
    return s or "col"


# =============================================================================
# Per-column profiling
# =============================================================================

def _summarize(view: str) -> list[dict]:
    """One-pass SUMMARIZE: type, min/max, approx_unique, null % per column."""
    return _rows_as_dicts(duckdb.sql(f"SUMMARIZE SELECT * FROM {_q(view)}"))


def _sample_values(view: str, col: str) -> list:
    rel = duckdb.sql(
        f"SELECT DISTINCT {_q(col)} AS v FROM {_q(view)} "
        f"WHERE {_q(col)} IS NOT NULL LIMIT {MAX_SAMPLE_VALUES}"
    )
    return [_fmt_value(r[0]) for r in rel.fetchall()]


def _varchar_quality(view: str, col: str) -> dict:
    """Pattern/quality counters for one VARCHAR column, in a single scan."""
    c = _q(col)
    pattern_exprs = ", ".join(
        f"count(*) FILTER (regexp_matches({c}, {_lit(rx)})) AS {name}"
        for name, rx in _TEMPORAL_PATTERNS.items()
    )
    null_like_list = ", ".join(_lit(v) for v in _NULL_LIKE)
    row = _rows_as_dicts(duckdb.sql(f"""
        SELECT
            count({c}) AS non_null,
            count(*) FILTER (regexp_matches({c}, {_lit(_NUMERIC_RE)})) AS numeric_like,
            count(*) FILTER (regexp_matches({c}, {_lit(_INTEGER_RE)})) AS integer_like,
            count(*) FILTER ({c} != trim({c})) AS whitespace,
            count(*) FILTER (lower(trim({c})) IN ({null_like_list})) AS null_like,
            {pattern_exprs}
        FROM {_q(view)}
    """))[0]
    return {k: int(v or 0) for k, v in row.items()}


def _column_profile(view: str, summary: dict, total_rows: int) -> dict:
    col = summary["column_name"]
    ctype = str(summary["column_type"])
    null_pct = float(summary.get("null_percentage") or 0.0)
    approx_unique = int(summary.get("approx_unique") or 0)
    non_null = int(round(total_rows * (1 - null_pct / 100.0)))

    prof = {
        "name": col,
        "type": ctype,
        "null_pct": round(null_pct, 2),
        "approx_unique": approx_unique,
        "min": _fmt_value(summary.get("min")),
        "max": _fmt_value(summary.get("max")),
        "samples": _sample_values(view, col),
    }

    flags: list[str] = []
    if non_null > 0 and approx_unique <= 1:
        flags.append("constant")
    # approx_unique is HLL — use it as a cheap screen, confirm exactly.
    if non_null > 0 and null_pct == 0 and approx_unique >= 0.9 * non_null:
        distinct = duckdb.sql(
            f"SELECT count(DISTINCT {_q(col)}) FROM {_q(view)}"
        ).fetchone()[0]
        if distinct == non_null:
            flags.append("unique")

    nested = any(t in ctype for t in ("STRUCT", "MAP", "[]", "LIST", "UNION"))
    if nested:
        flags.append("nested")
        prof["flags"] = flags
        return prof

    if ctype in _TEMPORAL_DUCK_TYPES:
        flags.append("temporal")

    if ctype == "VARCHAR" and non_null > 0:
        q = _varchar_quality(view, col)
        nn = max(q["non_null"], 1)
        if q["numeric_like"] >= 0.95 * nn:
            flags.append("integer_as_string" if q["integer_like"] == q["numeric_like"]
                         else "number_as_string")
        if q["null_like"] > 0:
            flags.append("null_like_strings")
            prof["null_like_count"] = q["null_like"]
        if q["whitespace"] > 0:
            flags.append("untrimmed")
        matched = {name: q[name] for name in _TEMPORAL_PATTERNS if q[name] > 0}
        dominant = [n for n, cnt in matched.items() if cnt >= 0.95 * nn]
        if dominant:
            flags.append("temporal")
            prof["temporal_pattern"] = dominant[0]
        else:
            significant = [n for n, cnt in matched.items() if cnt >= 0.05 * nn]
            if len(significant) > 1:
                flags.append("mixed_temporal_granularity")
                prof["temporal_patterns"] = {n: matched[n] for n in significant}

    prof["flags"] = flags
    return prof


# =============================================================================
# Fragment schema variance
# =============================================================================

def _fragment_variance(paths: list[str], rels: list[str]) -> list[str]:
    """DESCRIBE each fragment separately; report drift vs the first one.

    A merged read (union_by_name / widening) can hide per-file differences —
    'fragment 37 grew a column' is a real failure mode. Capped so a
    5000-fragment asset doesn't take forever; the cap is reported.
    """
    alerts = []
    if len(paths) < 2:
        return alerts
    if len(paths) > MAX_FRAGMENT_DESCRIBES:
        alerts.append(
            f"fragment variance check skipped: {len(paths)} fragments > "
            f"cap {MAX_FRAGMENT_DESCRIBES} (merged profile may hide per-file drift)"
        )
        return alerts

    schemas = {}
    for rel_name, path in zip(rels, paths):
        reader = _reader_for(rel_name)
        rows = _rows_as_dicts(duckdb.sql(f"DESCRIBE SELECT * FROM {reader}([{_lit(path)}])"))
        schemas[rel_name] = [(r["column_name"], str(r["column_type"])) for r in rows]

    baseline_name, baseline = next(iter(schemas.items()))
    for name, schema in schemas.items():
        if schema == baseline:
            continue
        base_cols, cols = dict(baseline), dict(schema)
        added = sorted(set(cols) - set(base_cols))
        removed = sorted(set(base_cols) - set(cols))
        retyped = sorted(k for k in cols.keys() & base_cols.keys() if cols[k] != base_cols[k])
        detail = "; ".join(filter(None, [
            f"added {added}" if added else "",
            f"missing {removed}" if removed else "",
            f"retyped {retyped}" if retyped else "",
            "column order differs" if not (added or removed or retyped) else "",
        ]))
        alerts.append(f"fragment schema drift: {name} vs {baseline_name}: {detail}")
    return alerts


# =============================================================================
# Draft contract + SQL skeleton
# =============================================================================

def _suggest(col: dict) -> tuple[str, str, str]:
    """(published_name, published_type, select_expr) suggestion for a column."""
    src, ctype, flags = col["name"], col["type"], col.get("flags", [])
    name = _snake_case(src)
    expr = _q(src)

    if "integer_as_string" in flags:
        return name, "BIGINT", f"CAST({expr} AS BIGINT)"
    if "number_as_string" in flags:
        return name, "DOUBLE", f"CAST({expr} AS DOUBLE)"
    if col.get("temporal_pattern") == "date":
        return name, "DATE", f"CAST({expr} AS DATE)"
    if col.get("temporal_pattern") == "timestamp":
        return name, "TIMESTAMP", f"CAST({expr} AS TIMESTAMP)"
    return name, ctype, expr


def _build_draft(asset_id: str, columns: list[dict]) -> dict:
    """Suggested contract from the profile. The draft is a starting point for
    curation, never a finished artifact — descriptions are empty, key is a
    guess, and every suggested cast needs a human/agent eye."""
    used: set[str] = set()
    entries = []
    for col in columns:
        name, ptype, expr = _suggest(col)
        while name in used:
            name += "_"
        used.add(name)
        entries.append({
            "source": col["name"],
            "name": name,
            "type": ptype,
            "expr": expr,
            "flags": col.get("flags", []),
        })

    temporal = next(
        (e["name"] for e, c in zip(entries, columns) if "temporal" in c.get("flags", [])),
        None,
    )
    key_candidates = [e["name"] for e, c in zip(entries, columns) if "unique" in c.get("flags", [])]
    return {"columns": entries, "temporal": temporal, "key_candidates": key_candidates}


def _draft_sql_text(asset_id: str, draft: dict) -> str:
    width = max((len(e["expr"]) + len(e["name"]) + 4) for e in draft["columns"])
    lines = [f"-- Draft transform for {asset_id} — generated by subsets_utils.profile.",
             "-- CURATE: verify names, casts, and drop columns that shouldn't publish.",
             "SELECT"]
    for i, e in enumerate(draft["columns"]):
        comma = "," if i < len(draft["columns"]) - 1 else ""
        select = f"    {e['expr']} AS {e['name']}{comma}"
        note = " ".join(e["flags"])
        lines.append(f"{select:<{width + 12}}-- {note}" if note else select)
    lines.append(f'FROM {_q(asset_id)}')
    return "\n".join(lines) + "\n"


def _draft_yml_text(asset_id: str, draft: dict) -> str:
    lines = [f"# Draft contract for {asset_id} — generated by subsets_utils.profile.",
             "# CURATE: descriptions, key (grain), temporal, types."]
    if draft["key_candidates"]:
        lines.append(f"# unique-column candidates: {draft['key_candidates']}")
    lines.append("# key: []            # TODO declare the grain ([] = explicitly keyless)")
    if draft["temporal"]:
        lines.append(f"temporal: {draft['temporal']}")
    else:
        lines.append("# temporal:          # TODO name the observation-period column, if any")
    lines.append("columns:")
    for e in draft["columns"]:
        lines.append(f"  - name: {e['name']}")
        lines.append(f"    type: {e['type']}")
        lines.append(f"    description: \"\"  # source: {e['source']}")
    return "\n".join(lines) + "\n"


# =============================================================================
# Asset profiling
# =============================================================================

def profile_asset(asset_id: str, sample: int | None = SAMPLE_DEFAULT) -> dict:
    """Profile one raw asset through the runtime's own read path. Never raises."""
    try:
        return _profile_asset(asset_id, sample)
    except Exception as e:  # noqa: BLE001 — error profiles keep sweeps alive
        return {"asset": asset_id, "error": f"{type(e).__name__}: {e}"}


def _profile_asset(asset_id: str, sample: int | None) -> dict:
    rels, clause = _read_clause(asset_id)
    view, pview = "__profile_full", "__profile"
    duckdb.sql(f"CREATE OR REPLACE TEMP VIEW {view} AS SELECT * FROM {clause}")

    total_rows = duckdb.sql(f"SELECT count(*) FROM {_q(view)}").fetchone()[0]
    sampled = sample is not None and total_rows > sample
    body = f"SELECT * FROM {_q(view)}" + (f" LIMIT {sample}" if sampled else "")
    duckdb.sql(f"CREATE OR REPLACE TEMP VIEW {pview} AS {body}")

    summaries = _summarize(pview)
    columns = [_column_profile(pview, s, min(total_rows, sample) if sampled else total_rows)
               for s in summaries]

    # Fragment paths are embedded in the clause; re-derive them the same way
    # _read_clause built them (reader(['p1', 'p2', ...])).
    paths = re.findall(r"'((?:[^']|'')*)'", clause)

    alerts = []
    if total_rows == 0:
        alerts.append("zero rows — transform would fail its correctness gate")
    if len(columns) > WIDE_TABLE_ALERT:
        alerts.append(f"wide table: {len(columns)} columns > {WIDE_TABLE_ALERT} "
                      "(pivoted upstream? consider unpivoting in the download fn)")
    nested_cols = [c["name"] for c in columns if "nested" in c.get("flags", [])]
    if nested_cols:
        alerts.append(f"nested column(s) {nested_cols[:10]} — the SQL must unnest "
                      "or the download fn should flatten")
    alerts.extend(_fragment_variance(paths, rels))

    return {
        "asset": asset_id,
        "treatment": {
            "files": rels,
            "file_count": len(rels),
            "read_clause": clause[:300],
            "rows_profiled": min(total_rows, sample) if sampled else total_rows,
            "sampled": sampled,
        },
        "envelope": {
            "rows": total_rows,
            "columns": len(columns),
            "nested_columns": nested_cols,
        },
        "columns": columns,
        "alerts": alerts,
        "draft": _build_draft(asset_id, columns),
    }


# =============================================================================
# CLI
# =============================================================================

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m subsets_utils.profile",
        description="Profile raw asset(s) through the transform runtime's read path.",
    )
    parser.add_argument("assets", nargs="+", help="raw asset id(s) (= download NodeSpec ids)")
    parser.add_argument("--sample", type=int, default=SAMPLE_DEFAULT,
                        help=f"row cap for profiling queries (default {SAMPLE_DEFAULT:_})")
    parser.add_argument("--full", action="store_true", help="profile all rows (no sampling)")
    parser.add_argument("--draft-dir", help="write <asset>.sql + <asset>.yml drafts here")
    parser.add_argument("--out", help="write JSON profile(s) to this file instead of stdout")
    args = parser.parse_args(argv)

    _configure()
    sample = None if args.full else args.sample

    profiles = [profile_asset(a, sample) for a in args.assets]

    if args.draft_dir:
        from pathlib import Path
        draft_dir = Path(args.draft_dir)
        draft_dir.mkdir(parents=True, exist_ok=True)
        for p in profiles:
            if "error" in p:
                print(f"[profile] {p['asset']}: skipping draft ({p['error']})", file=sys.stderr)
                continue
            (draft_dir / f"{p['asset']}.sql").write_text(_draft_sql_text(p["asset"], p["draft"]))
            (draft_dir / f"{p['asset']}.yml").write_text(_draft_yml_text(p["asset"], p["draft"]))
            print(f"[profile] draft written: {draft_dir}/{p['asset']}.{{sql,yml}}", file=sys.stderr)

    payload = profiles[0] if len(profiles) == 1 else profiles
    text = json.dumps(payload, indent=1, ensure_ascii=False, default=str)
    if args.out:
        from pathlib import Path
        Path(args.out).write_text(text)
        print(f"[profile] wrote {args.out}", file=sys.stderr)
    else:
        print(text)

    return 1 if any("error" in p for p in profiles) else 0


if __name__ == "__main__":
    sys.exit(main())
