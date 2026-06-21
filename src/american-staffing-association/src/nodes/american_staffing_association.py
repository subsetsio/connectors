"""American Staffing Association — ASA Data Dashboard connector.

The ASA Data Dashboard is powered by four public Google Sheets workbooks, one
per dashboard panel. Each workbook is downloadable as CSV via the public Google
Visualization (gviz) export endpoint with no authentication. Each panel is a
distinct dataset with its own column schema, so this is a simple connector:
one explicit download spec + one transform per panel.

Shape: stateless full re-pull. The workbooks are tiny (a few thousand rows
total, well under 5MB) and carry revisions in place, so we re-fetch each
workbook in full every run and overwrite — no watermarks, no incremental
state. The gviz CSV is faithful-but-messy (blank header cells, merged-cell
artifacts, '$'/','/'%' formatting), so the download fns parse positionally to
clean column names but keep VALUES as raw strings (blank -> null); the
transform SQL is the typing/cleaning gate.
"""

import csv
import io

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
)

GVIZ = "https://docs.google.com/spreadsheets/d/{sid}/gviz/tq?tqx=out:csv"


@transient_retry()
def _download_csv(spreadsheet_id: str, tab: str | None) -> list[list[str]]:
    url = GVIZ.format(sid=spreadsheet_id)
    params = {"sheet": tab} if tab else None
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    text = resp.content.decode("utf-8", "replace")
    if text.lstrip().startswith("<"):
        # gviz returns an HTML error page (not CSV) when a sheet/tab is missing.
        raise RuntimeError(
            f"gviz returned HTML, not CSV, for {spreadsheet_id} tab={tab!r}"
        )
    return list(csv.reader(io.StringIO(text)))


def _clean(cell: str) -> str | None:
    v = cell.strip()
    return v if v else None


# --- ASA Staffing Index (weekly) -------------------------------------------
# Columns (positional; header has blank cells):
#   0 week-of-year index, 1 "Week ending", 2 noisy mis-scaled change (dropped),
#   3 ASA Staffing Index, 4 decimal w/w change, 5 percent w/w change (dropped,
#   redundant with col4), 6 "Four Week Average", 7 trailing blank.
def fetch_staffing_index(node_id: str) -> None:
    rows = _download_csv("1R3aWI9pVba31-xoqhn-4OwsVrgZHXxEJQKpNYg2Vmn4",
                         "52 week 2006-present")
    out = []
    for r in rows[1:]:
        if len(r) < 7:
            continue
        out.append({
            "week_ending": _clean(r[1]),
            "staffing_index": _clean(r[3]),
            "wow_change": _clean(r[4]),
            "four_week_average": _clean(r[6]),
        })
    save_raw_ndjson(out, node_id)


# --- BLS monthly staffing employment series --------------------------------
# Columns: 0 "Series ID", 1 "Year" ("1990 Jan"), 2 "Period" ("M01"),
#          3 "Value", 4 trailing blank.
def fetch_bls_monthly(node_id: str) -> None:
    rows = _download_csv("15J3PsNHBmJ2W0-pzzkntlyUL_UiGexOhkBj2hiDxaZ8", None)
    out = []
    for r in rows[1:]:
        if len(r) < 4:
            continue
        year_field = _clean(r[1])  # e.g. "1990 Jan"
        year = year_field.split()[0] if year_field else None
        out.append({
            "series_id": _clean(r[0]),
            "year": year,
            "period": _clean(r[2]),
            "value": _clean(r[3]),
        })
    save_raw_ndjson(out, node_id)


# --- ASA Staffing Employment & Sales Survey (quarterly) --------------------
# Columns: 0 Year, 1 Quarter, 2 Sales ($), 3 Sales QoQ (%), 4 Sales YoY (%),
#          5 Payroll ($), 6 Payroll QoQ (%), 7 Payroll YoY (%),
#          8 AWE (number), 9 AWE QoQ (%), 10 AWE YoY (%).
def fetch_quarterly_employment_sales(node_id: str) -> None:
    rows = _download_csv("1VyY2-rTKSfqcEUGFJrm5fGPMI0n2TGAzBy1WRJbEyVk", None)
    cols = ["year", "quarter", "sales", "sales_qoq", "sales_yoy",
            "payroll", "payroll_qoq", "payroll_yoy",
            "awe", "awe_qoq", "awe_yoy"]
    out = []
    for r in rows[1:]:
        if len(r) < 11:
            continue
        out.append({c: _clean(r[i]) for i, c in enumerate(cols)})
    save_raw_ndjson(out, node_id)


# --- GDP quarterly projections ---------------------------------------------
# Columns: 0 Quarter, 1 Year, 2 First (%), 3 Second (%), 4 Third (%),
#          5 Revised/Final (%), then many trailing blank columns.
def fetch_gdp_projections(node_id: str) -> None:
    rows = _download_csv("1-HnFJe9CwB4BCjcubGKY8RBVzyW65anXAWs6Zdomaxg", None)
    out = []
    for r in rows[1:]:
        if len(r) < 6:
            continue
        out.append({
            "quarter": _clean(r[0]),
            "year": _clean(r[1]),
            "first_estimate": _clean(r[2]),
            "second_estimate": _clean(r[3]),
            "third_estimate": _clean(r[4]),
            "revised_final": _clean(r[5]),
        })
    save_raw_ndjson(out, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="american-staffing-association-staffing-index",
             fn=fetch_staffing_index, kind="download"),
    NodeSpec(id="american-staffing-association-bls-monthly-employment",
             fn=fetch_bls_monthly, kind="download"),
    NodeSpec(id="american-staffing-association-quarterly-employment-sales",
             fn=fetch_quarterly_employment_sales, kind="download"),
    NodeSpec(id="american-staffing-association-gdp-quarterly-projections",
             fn=fetch_gdp_projections, kind="download"),
]


# Currency/number-with-commas cleaner used in several transforms.
def _num(col: str) -> str:
    return f"TRY_CAST(replace(replace(replace(trim({col}), '$', ''), ',', ''), ' ', '') AS DOUBLE)"


def _pct(col: str) -> str:
    return f"TRY_CAST(replace({col}, '%', '') AS DOUBLE)"


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="american-staffing-association-staffing-index-transform",
        deps=["american-staffing-association-staffing-index"],
        sql='''
            SELECT
                strptime(week_ending, '%-m/%-d/%Y')::DATE AS week_ending,
                CAST(staffing_index AS DOUBLE)            AS staffing_index,
                TRY_CAST(wow_change AS DOUBLE)            AS wow_change,
                TRY_CAST(four_week_average AS DOUBLE)     AS four_week_average
            FROM "american-staffing-association-staffing-index"
            WHERE week_ending IS NOT NULL
              AND staffing_index IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="american-staffing-association-bls-monthly-employment-transform",
        deps=["american-staffing-association-bls-monthly-employment"],
        sql='''
            SELECT
                series_id,
                CAST(year AS INTEGER)                            AS year,
                period,
                CAST(substr(period, 2, 2) AS INTEGER)            AS month,
                make_date(CAST(year AS INTEGER),
                          CAST(substr(period, 2, 2) AS INTEGER), 1) AS month_start,
                CAST(value AS DOUBLE)                            AS value
            FROM "american-staffing-association-bls-monthly-employment"
            WHERE series_id IS NOT NULL
              AND year IS NOT NULL
              AND period IS NOT NULL
              AND value IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="american-staffing-association-quarterly-employment-sales-transform",
        deps=["american-staffing-association-quarterly-employment-sales"],
        sql=f'''
            SELECT
                CAST(year AS INTEGER)        AS year,
                CAST(quarter AS INTEGER)     AS quarter,
                {_num('sales')}              AS sales,
                {_pct('sales_qoq')}          AS sales_qoq_pct,
                {_pct('sales_yoy')}          AS sales_yoy_pct,
                {_num('payroll')}            AS payroll,
                {_pct('payroll_qoq')}        AS payroll_qoq_pct,
                {_pct('payroll_yoy')}        AS payroll_yoy_pct,
                {_num('awe')}                AS awe,
                {_pct('awe_qoq')}            AS awe_qoq_pct,
                {_pct('awe_yoy')}            AS awe_yoy_pct
            FROM "american-staffing-association-quarterly-employment-sales"
            WHERE year IS NOT NULL AND quarter IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="american-staffing-association-gdp-quarterly-projections-transform",
        deps=["american-staffing-association-gdp-quarterly-projections"],
        sql=f'''
            SELECT
                CAST(year AS INTEGER)        AS year,
                CAST(quarter AS INTEGER)     AS quarter,
                {_pct('first_estimate')}     AS first_estimate_pct,
                {_pct('second_estimate')}    AS second_estimate_pct,
                {_pct('third_estimate')}     AS third_estimate_pct,
                {_pct('revised_final')}      AS revised_final_pct
            FROM "american-staffing-association-gdp-quarterly-projections"
            WHERE year IS NOT NULL AND quarter IS NOT NULL
        ''',
    ),
]
