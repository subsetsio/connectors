"""Freedom in the World — indicator-level panel (FIW all-data workbook)."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import (
    _NOTES,
    _data_sheet,
    _find_header_row,
    _num,
    _sheet_rows,
    _txt,
    _workbook,
    _year,
)

_URL = "https://freedomhouse.org/sites/default/files/2025-02/All_data_FIW_2013-2024.xlsx"

_FIW_ALL_RENAME = {
    "Country/Territory": "country_territory",
    "Region": "region",
    "C/T": "ct",
    "Edition": "year",
    "Status": "status",
    "PR rating": "pr_rating",
    "CL rating": "cl_rating",
    "Add Q": "add_q",
    "Add A": "add_a",
    "PR": "pr_aggregate",
    "CL": "cl_aggregate",
    "Total": "total",
}
_FIW_ALL_STR = {"country_territory", "region", "ct", "status"}


def fetch_fiw_all_data(node_id: str) -> None:
    """Freedom in the World indicator-level panel — one row per country/territory
    per edition year, with the 25 sub-indicators (a1..g4), group aggregates
    (a..g), the PR/CL ratings, the PR/CL aggregate sums and the 0-100 total."""
    wb = _workbook(_URL)
    ws = _data_sheet(wb, exclude_substrings=_NOTES)
    rows = _sheet_rows(ws)
    h = _find_header_row(rows, "Country/Territory")
    header = [_txt(c) for c in rows[h]]
    keys = [_FIW_ALL_RENAME.get(col, (col or "").strip().lower()) for col in header]
    out = []
    for raw in rows[h + 1:]:
        rec = {}
        for k, v in zip(keys, raw):
            if not k:
                continue
            if k == "year":
                rec[k] = _year(v)
            elif k in _FIW_ALL_STR:
                rec[k] = _txt(v)
            else:
                rec[k] = _num(v)
        if rec.get("country_territory") and rec.get("year") is not None:
            out.append(rec)
    wb.close()
    save_raw_ndjson(out, node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="freedom-house-fiw-all-data", fn=fetch_fiw_all_data, kind="download"),
]

_TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="freedom-house-fiw-all-data-transform",
        deps=["freedom-house-fiw-all-data"],
        sql='''
            SELECT
                country_territory,
                region,
                ct,
                CAST(year AS INTEGER) AS year,
                status,
                pr_rating, cl_rating,
                a1, a2, a3, a,
                b1, b2, b3, b4, b,
                c1, c2, c3, c,
                add_q, add_a,
                pr_aggregate,
                d1, d2, d3, d4, d,
                e1, e2, e3, e,
                f1, f2, f3, f4, f,
                g1, g2, g3, g4, g,
                cl_aggregate,
                total
            FROM "freedom-house-fiw-all-data"
            WHERE country_territory IS NOT NULL AND year IS NOT NULL
        ''',
    ),
]
