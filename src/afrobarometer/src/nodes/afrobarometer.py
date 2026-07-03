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

import pyarrow as pa
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet, raw_parquet_writer

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

VALUES_FLUSH_ROWS = 25000          # buffer size before a streamed row-group write
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

    One ODA `question` call per variable (country x round matrix), streamed to a
    single parquet asset so memory stays bounded over ~4k variables.
    """
    sid = open_session()
    catalog = build_catalog(sid)
    variables = catalog["variables"]
    saids = ",".join(str(s) for s in catalog["country_said"].values())

    total = len(variables)
    if total == 0:
        raise RuntimeError("no survey variables discovered from ODA index")

    skipped = 0
    written = 0
    buffer = []
    with raw_parquet_writer(node_id, VALUES_SCHEMA) as writer:
        for i, (vc, rec) in enumerate(sorted(variables.items())):
            rec = dict(rec, _vc=vc)
            try:
                payload = fetch_question_timeseries(
                    sid, rec["qid"], rec["round_id"], saids
                )
                if not payload.get("success"):
                    # App-level rejection (e.g. structure/admin variable that
                    # cannot be cross-tabulated). Skip this variable.
                    skipped += 1
                    continue
                buffer.extend(_parse_question(payload, rec))
            except Exception as exc:  # network/HTTP after retries, or bad shape
                skipped += 1
                print(
                    "  ! skip variable %s (qid=%s): %s: %s"
                    % (vc, rec["qid"], type(exc).__name__, exc)
                )

            if len(buffer) >= VALUES_FLUSH_ROWS:
                writer.write_table(pa.Table.from_pylist(buffer, schema=VALUES_SCHEMA))
                written += len(buffer)
                buffer = []

            if (i + 1) % 200 == 0:
                print(
                    "  ... %d/%d variables, %d rows written, %d skipped"
                    % (i + 1, total, written + len(buffer), skipped)
                )

        if buffer:
            writer.write_table(pa.Table.from_pylist(buffer, schema=VALUES_SCHEMA))
            written += len(buffer)

    print("  values: %d rows, %d/%d variables skipped" % (written, skipped, total))
    if skipped > total * MAX_SKIP_FRACTION:
        raise RuntimeError(
            "skipped %d of %d variables (>%.0f%%) — likely a systemic ODA failure"
            % (skipped, total, MAX_SKIP_FRACTION * 100)
        )
    if written == 0:
        raise RuntimeError("values pull produced 0 rows")


DOWNLOAD_SPECS = [
    NodeSpec(id="afrobarometer-questions", fn=fetch_questions, kind="download"),
    NodeSpec(id="afrobarometer-values", fn=fetch_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="afrobarometer-questions-transform",
        deps=["afrobarometer-questions"],
        key=("variable_code",),
        sql='''
            SELECT
                variable_code,
                CAST(question_id AS BIGINT)      AS question_id,
                title,
                section,
                CAST(n_rounds AS INTEGER)        AS n_rounds,
                round_nums,
                CAST(latest_round_num AS INTEGER) AS latest_round_num
            FROM "afrobarometer-questions"
            WHERE variable_code IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="afrobarometer-values-transform",
        deps=["afrobarometer-values"],
        key=("variable_code", "country", "round_num", "answer_code"),
        temporal="round_num",
        sql='''
            SELECT
                variable_code,
                CAST(question_id AS BIGINT)  AS question_id,
                question_title,
                section,
                country,
                CAST(round_num AS INTEGER)   AS round_num,
                round_label,
                CAST(answer_code AS INTEGER) AS answer_code,
                answer_label,
                is_missing,
                CAST(weighted_n AS DOUBLE)   AS weighted_n,
                CAST(pct_valid AS DOUBLE)    AS pct_valid
            FROM "afrobarometer-values"
            WHERE pct_valid IS NOT NULL
              AND variable_code IS NOT NULL
              AND country IS NOT NULL
              AND round_num IS NOT NULL
        ''',
    ),
]
