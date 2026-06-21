"""NY Fed — SOMA holdings summary (per as-of-date aggregate totals)."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import get_json, project

_SUMMARY_FIELDS = (
    "asOfDate", "bills", "notesbonds", "tips", "frn",
    "tipsInflationCompensation", "mbs", "cmbs", "agencies", "total",
)


def fetch_soma_summary(node_id: str) -> None:
    payload = get_json("soma/summary.json")
    summary = payload.get("soma", {}).get("summary", [])
    rows = [project(r, _SUMMARY_FIELDS) for r in summary]
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="ny-fed-soma-summary", fn=fetch_soma_summary, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ny-fed-soma-summary-transform",
        deps=["ny-fed-soma-summary"],
        sql='''
            SELECT
                TRY_CAST(asOfDate AS DATE)           AS as_of_date,
                TRY_CAST(bills AS DOUBLE)            AS bills,
                TRY_CAST(notesbonds AS DOUBLE)      AS notes_bonds,
                TRY_CAST(tips AS DOUBLE)            AS tips,
                TRY_CAST(frn AS DOUBLE)             AS frn,
                TRY_CAST(tipsInflationCompensation AS DOUBLE) AS tips_inflation_compensation,
                TRY_CAST(mbs AS DOUBLE)            AS mbs,
                TRY_CAST(cmbs AS DOUBLE)           AS cmbs,
                TRY_CAST(agencies AS DOUBLE)       AS agencies,
                TRY_CAST(total AS DOUBLE)          AS total
            FROM "ny-fed-soma-summary"
            WHERE TRY_CAST(asOfDate AS DATE) IS NOT NULL
        ''',
    ),
]
