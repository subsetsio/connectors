"""HPES survey history panel: pivot of expected home-price change (no auth)."""

import re

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import _ffill, _load_rows, _num

# data-and-insights page slug + constant filename prefix (HPES page hosts two).
_PAGE = ("home-price-expectations-survey-hpes", "hpes-survey-history-panel")


def fetch_hpes_history(node_id: str) -> None:
    """HPES survey history panel: a pivot of expected home-price change.
    row 8 = metric block (Year-over-Year / Cumulative, merged), row 10 =
    survey group ('YYYY Surveys', merged), row 12 = survey period
    (month or quarter), col 1 = target year; cells are the forecast value.
    Melt every numeric cell to long format, generic to extra blocks/years."""
    _, rows = _load_rows(node_id, *_PAGE)
    ncols = max(len(r) for r in rows[:13])
    metrics = _ffill(rows[8], ncols)
    surveys = _ffill(rows[10], ncols)
    periods = [None] * ncols
    for i in range(ncols):
        v = rows[12][i] if i < len(rows[12]) else None
        periods[i] = str(v).strip() if v is not None and str(v).strip() else None
    out = []
    for r in rows[13:]:
        ty = _num(r[1]) if len(r) > 1 else None
        if ty is None:  # below the year block (footnotes)
            continue
        target_year = int(ty)
        for c in range(2, ncols):
            period = periods[c]
            survey = surveys[c]
            metric = metrics[c]
            if not period or not survey:
                continue
            val = _num(r[c]) if c < len(r) else None
            if val is None:
                continue
            sy = re.match(r"(\d{4})", survey)
            out.append({
                "metric": metric,
                "survey_year": int(sy.group(1)) if sy else None,
                "survey_period": period,
                "target_year": target_year,
                "value": val,
            })
    if not out:
        raise AssertionError(f"{node_id}: parsed 0 HPES history rows")
    save_raw_ndjson(out, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="fannie-mae-hpes-survey-history-panel", fn=fetch_hpes_history, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fannie-mae-hpes-survey-history-panel-transform",
        deps=["fannie-mae-hpes-survey-history-panel"],
        sql='''
            SELECT
                CAST(metric AS VARCHAR)        AS metric,
                CAST(survey_year AS INTEGER)   AS survey_year,
                CAST(survey_period AS VARCHAR) AS survey_period,
                CAST(target_year AS INTEGER)   AS target_year,
                CAST(value AS DOUBLE)          AS value
            FROM "fannie-mae-hpes-survey-history-panel"
            WHERE value IS NOT NULL
        ''',
    ),
]
