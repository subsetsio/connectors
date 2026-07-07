"""Afrobarometer connector — public Online Data Analysis (ODA) web service.

Two published tables (the rank-accepted entity union):

  * questions : reference catalog, one row per distinct survey variable across
                the 10 survey rounds (variable code, title, section, round span).
  * values    : long-format aggregated statistics — one row per
                (variable, country, round, answer category) with the weighted
                frequency and valid percentage. Built by calling the ODA
                `question` endpoint once per variable in time-series +
                country-cross mode, which returns the whole country x round
                matrix for that variable in a single request.

The data is a full snapshot that changes only when Afrobarometer releases a new
survey round (every ~2-3 years), so both nodes do a stateless full re-pull and
overwrite. Freshness/cadence is the maintain step's concern.
"""

import os

import pyarrow as pa
from subsets_utils import NodeSpec, list_raw_fragments, save_raw_parquet

from utils import (
    build_catalog,
    fetch_question_timeseries,
    open_session,
    round_num,
)

QUESTIONS_SCHEMA = pa.schema([
    ("variable_code", pa.string()),
    ("question_id", pa.int64()),
    ("title", pa.string()),
    ("section", pa.string()),
    ("n_rounds", pa.int32()),
    ("round_nums", pa.string()),
    ("latest_round_num", pa.int32()),
])

VALUES_SCHEMA = pa.schema([
    ("variable_code", pa.string()),
    ("question_id", pa.int64()),
    ("question_title", pa.string()),
    ("section", pa.string()),
    ("country", pa.string()),
    ("round_num", pa.int32()),
    ("round_label", pa.string()),
    ("answer_code", pa.int32()),
    ("answer_label", pa.string()),
    ("is_missing", pa.bool_()),
    ("weighted_n", pa.float64()),
    ("pct_valid", pa.float64()),
])

VALUES_FRAGMENT_VARIABLES = 100    # commit progress often enough for CI continuation
MAX_SKIP_FRACTION = 0.05           # systemic-failure guard for the values pull


def fetch_questions(node_id: str) -> None:
    """Reference catalog of survey variables (one row per distinct code)."""
    sid = open_session()
    catalog = build_catalog(sid)
    variables = catalog["variables"]

    rows = []
    for vc, rec in sorted(variables.items()):
        nums = sorted(rec["round_nums"])
        rows.append({
            "variable_code": vc,
            "question_id": rec["qid"],
            "title": rec["title"],
            "section": rec["group"],
            "n_rounds": rec["n_rounds"],
            "round_nums": ",".join(str(n) for n in nums),
            "latest_round_num": nums[-1] if nums else None,
        })

    table = pa.Table.from_pylist(rows, schema=QUESTIONS_SCHEMA)
    save_raw_parquet(table, node_id)


def _parse_question(payload: dict, rec: dict):
    """Flatten one ODA question response into long rows. Drops cells where the
    variable was not surveyed (n == 0 and pct == 0)."""
    result = payload.get("resultado") or {}
    tables = result.get("tables") or []
    countries = [
        (c.get("shortLabel") or "").strip()
        for c in result.get("etiqCols2") or []
    ]
    # round columns: (label, round_num, is_total)
    cols = []
    for c in result.get("etiqCols") or []:
        lbl = (c.get("shortLabel") or "").strip()
        cols.append((lbl, round_num(lbl), bool(c.get("total")) or lbl == "(N)"))

    out = []
    for ci, tbl in enumerate(tables):
        country = countries[ci] if ci < len(countries) else None
        if not country or country == "(N)":
            continue
        for ans in tbl.get("rows") or []:
            if ans.get("total"):
                continue
            freq = ans.get("frecuenciasN") or []
            pct = ans.get("porcentajeV") or []
            answer_code = ans.get("valorCat")
            answer_label = ans.get("longLabel") or ans.get("shortLabel") or ""
            is_missing = bool(ans.get("missing"))
            for j, (lbl, rnum, is_total) in enumerate(cols):
                if is_total or rnum is None:
                    continue
                n = freq[j] if j < len(freq) else None
                p = pct[j] if j < len(pct) else None
                if (not n) and (not p):
                    continue
                out.append({
                    "variable_code": rec["_vc"],
                    "question_id": rec["qid"],
                    "question_title": rec["title"],
                    "section": rec["group"],
                    "country": country,
                    "round_num": rnum,
                    "round_label": lbl,
                    "answer_code": answer_code,
                    "answer_label": answer_label,
                    "is_missing": is_missing,
                    "weighted_n": float(n) if n is not None else None,
                    "pct_valid": float(p) if p is not None else None,
                })
    return out


def fetch_values(node_id: str) -> None:
    """Long-format aggregated statistics across every survey variable.

    One ODA `question` call per variable (country x round matrix), committed in
    deterministic parquet fragments. Cloud runs can hit their deadline on this
    source; fragments let continuation legs skip already committed chunks.
    """
    sid = open_session()
    catalog = build_catalog(sid)
    variables = sorted(catalog["variables"].items())
    saids = ",".join(str(s) for s in catalog["country_said"].values())

    total = len(variables)
    if total == 0:
        raise RuntimeError("no survey variables discovered from ODA index")

    run_id = os.environ.get("RUN_ID", "unknown")
    done = {
        frag
        for frag, meta in list_raw_fragments(node_id, "parquet").items()
        if meta.get("run_id") == run_id
    }
    skipped = 0
    written = 0
    processed = 0
    for start in range(0, total, VALUES_FRAGMENT_VARIABLES):
        chunk = variables[start:start + VALUES_FRAGMENT_VARIABLES]
        end = start + len(chunk)
        fragment = "part-%05d-%05d" % (start, end - 1)
        if fragment in done:
            print("  ... skip committed fragment %s" % fragment)
            continue

        rows = []
        chunk_skipped = 0
        for i, (vc, rec) in enumerate(chunk, start=start):
            rec = dict(rec, _vc=vc)
            try:
                payload = fetch_question_timeseries(
                    sid, rec["qid"], rec["round_id"], saids
                )
                if not payload.get("success"):
                    # App-level rejection (e.g. structure/admin variable that
                    # cannot be cross-tabulated). Skip this variable.
                    skipped += 1
                    chunk_skipped += 1
                    continue
                rows.extend(_parse_question(payload, rec))
            except Exception as exc:  # network/HTTP after retries, or bad shape
                skipped += 1
                chunk_skipped += 1
                print(
                    "  ! skip variable %s (qid=%s): %s: %s"
                    % (vc, rec["qid"], type(exc).__name__, exc)
                )

            processed += 1

        table = pa.Table.from_pylist(rows, schema=VALUES_SCHEMA)
        save_raw_parquet(table, node_id, fragment=fragment)
        written += len(rows)
        print(
            "  ... %d/%d variables, %d rows written, %d skipped "
            "(fragment %s: %d rows, %d skipped)"
            % (end, total, written, skipped, fragment, len(rows), chunk_skipped)
        )

    print(
        "  values: %d rows written this leg, %d/%d processed variables skipped"
        % (written, skipped, processed)
    )
    if processed and skipped > processed * MAX_SKIP_FRACTION:
        raise RuntimeError(
            "skipped %d of %d processed variables (>%.0f%%) - likely a systemic ODA failure"
            % (skipped, processed, MAX_SKIP_FRACTION * 100)
        )
    if written == 0 and not done:
        raise RuntimeError("values pull produced 0 rows")


DOWNLOAD_SPECS = [
    NodeSpec(id="afrobarometer-questions", fn=fetch_questions, kind="download"),
    NodeSpec(id="afrobarometer-values", fn=fetch_values, kind="download"),
]
