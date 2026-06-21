"""Bank Negara Malaysia — Overnight Policy Rate (OPR) subset.

Access pattern: year-iterated (/opr/year/{y}), one call per year from the
discovered start year through the current year. Each call returns the policy
decisions for that year. Stateless full re-pull.
"""
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import (
    PREFIX,
    _discover_start_year,
    _now,
    _parallel,
)


def _collect_opr():
    start = _discover_start_year(lambda y: f"opr/year/{y}")
    cur_year, _ = _now()
    tasks = [(y, f"opr/year/{y}") for y in range(start, cur_year + 1)]
    rows = []
    for _y, payload in _parallel(tasks):
        if not payload:
            continue
        for rec in payload.get("data") or []:
            rows.append({
                "year": rec.get("year"),
                "date": rec.get("date"),
                "change_in_opr": rec.get("change_in_opr"),
                "new_opr_level": rec.get("new_opr_level"),
            })
    return rows


def fetch_one(node_id: str) -> None:
    resource = node_id[len(PREFIX):]
    rows = _collect_opr()
    if not rows:
        raise RuntimeError(f"{resource}: collected 0 rows")
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{PREFIX}opr", fn=fetch_one, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{PREFIX}opr-transform",
        deps=[f"{PREFIX}opr"],
        sql=f'''
            SELECT CAST(date AS DATE)             AS date,
                   CAST(year AS INTEGER)          AS year,
                   CAST(change_in_opr AS DOUBLE)  AS change_in_opr,
                   CAST(new_opr_level AS DOUBLE)  AS new_opr_level
            FROM "{PREFIX}opr"
            WHERE date IS NOT NULL
            QUALIFY row_number() OVER (PARTITION BY date ORDER BY date) = 1
        ''',
    ),
]
