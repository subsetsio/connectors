"""NFIB SBET survey responses: long-format monthly answer-code distributions for
the SBET survey questions, via the getTrends2 proc.
"""

import datetime as _dt

import pyarrow as pa

from subsets_utils import save_raw_parquet, NodeSpec, SqlNodeSpec
from utils import _proc, _MIN_YEAR, _MAX_YEAR

# The SBET survey questions whose getTrends2 response is a real per-answer-code
# distribution. Excludes the two qver=2 derived views (rate_change_2,
# cap_ex_total_2) and the client-computed un_index, none of which getTrends2
# serves directly (they return empty). The base questions rate_change and
# cap_ex_total ARE included here.
_SURVEY_CODES = [
    "emp_count_change_expect", "cap_ex_expect", "inventory_expect", "bus_cond_expect",
    "sales_expect", "inventory_current", "job_opening_unfilled", "credit_access_expect",
    "expand_good", "earn_change", "sales_change", "price_change", "price_change_plan",
    "emp_count_change", "emp_comp_change", "emp_comp_change_expect", "rate_change",
    "inventory_change", "qualified_appl", "credit_access", "cap_ex_total", "top_issue",
    "expand_good_why", "earn_change_reason_down", "earn_change_reason_up",
]


def _parse_mdy(s):
    """getTrends2 monthyear is 'M/D/YYYY' (e.g. '5/1/2026') — a different
    format from getIndicators2, despite the same field name."""
    return _dt.datetime.strptime(s, "%m/%d/%Y").date()


def _split_answer(label):
    """'3. STAY THE SAME' -> (3, 'STAY THE SAME'); robust to missing code."""
    if ". " in label:
        head, tail = label.split(". ", 1)
        try:
            return int(head), tail.strip()
        except ValueError:
            return None, label.strip()
    return None, label.strip()


_SURVEY_SCHEMA = pa.schema([
    ("date", pa.date32()),
    ("question_code", pa.string()),
    ("question_text", pa.string()),
    ("answer_code", pa.int64()),
    ("answer_label", pa.string()),
    ("respondent_count", pa.int64()),
    ("total_per_question", pa.int64()),
    ("percent", pa.float64()),
])


def fetch_survey_responses(asset_id: str) -> None:
    cols = {k: [] for k in
            ("date", "question_code", "question_text", "answer_code",
             "answer_label", "respondent_count", "total_per_question", "percent")}
    for code in _SURVEY_CODES:
        rows = _proc("getTrends2", [
            ("minYear", _MIN_YEAR), ("minMonth", 1),
            ("maxYear", _MAX_YEAR), ("maxMonth", 12),
            ("questions", code), ("industry", ""), ("employee", ""), ("statev", ""),
        ])
        if not rows:
            # A previously-served question returning empty means the source
            # changed shape — fail loudly rather than publish a gap.
            raise ValueError(f"getTrends2 returned 0 rows for survey question '{code}'")
        for rec in rows:
            acode, alabel = _split_answer(rec.get("answer", ""))
            cols["date"].append(_parse_mdy(rec["monthyear"]))
            cols["question_code"].append(rec.get("resp_q_short") or code)
            cols["question_text"].append(rec.get("resp_q"))
            cols["answer_code"].append(acode)
            cols["answer_label"].append(alabel)
            cols["respondent_count"].append(rec.get("totalcount"))
            cols["total_per_question"].append(rec.get("total_per_question"))
            cols["percent"].append(rec.get("percent"))
    table = pa.table(cols, schema=_SURVEY_SCHEMA)
    save_raw_parquet(table, asset_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="nfib-survey-responses", fn=fetch_survey_responses),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nfib-survey-responses-transform",
        deps=("nfib-survey-responses",),
        sql='''
            SELECT
                date,
                question_code,
                question_text,
                answer_code,
                answer_label,
                respondent_count,
                total_per_question,
                percent
            FROM "nfib-survey-responses"
            ORDER BY question_code, date, answer_code
        ''',
    ),
]
