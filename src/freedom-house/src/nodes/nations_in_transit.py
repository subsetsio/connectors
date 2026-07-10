"""Nations in Transit — democracy panel."""

import re

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

_URL = "https://freedomhouse.org/sites/default/files/2024-05/All_Data_Nations_in_Transit_NIT_2005-2024_For_website.xlsx"


def _snake(s: str) -> str:
    return re.sub(r"_+", "_", re.sub(r"[^0-9a-z]+", "_", (s or "").strip().lower())).strip("_")


_NIT_STR = {"region", "country", "regime_classification"}


def fetch_nations_in_transit(node_id: str) -> None:
    """Nations in Transit democracy panel — one row per country per year: the 7
    category sub-scores, the 1-7 Democracy Score, the Democracy Percentage and
    the regime classification."""
    wb = _workbook(_URL)
    ws = _data_sheet(wb, exclude_substrings=_NOTES)
    rows = _sheet_rows(ws)
    h = _find_header_row(rows, "Region")
    keys = [_snake(_txt(c) or "") for c in rows[h]]
    out = []
    for raw in rows[h + 1:]:
        rec = {}
        for k, v in zip(keys, raw):
            if not k:
                continue
            if k == "year":
                rec[k] = _year(v)
            elif k in _NIT_STR:
                rec[k] = _txt(v)
            else:
                rec[k] = _num(v)
        if rec.get("country") and rec.get("year") is not None:
            out.append(rec)
    wb.close()
    save_raw_ndjson(out, node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="freedom-house-nations-in-transit", fn=fetch_nations_in_transit, kind="download"),
]

_TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="freedom-house-nations-in-transit-transform",
        deps=["freedom-house-nations-in-transit"],
        sql='''
            SELECT
                region,
                country,
                CAST(year AS INTEGER) AS year,
                national_democratic_governance,
                electoral_process,
                civil_society,
                independent_media,
                local_democratic_governance,
                judicial_framework_and_independence,
                corruption,
                democracy_score,
                democracy_percentage,
                democracy_percentage_rounded,
                regime_classification
            FROM "freedom-house-nations-in-transit"
            WHERE country IS NOT NULL AND year IS NOT NULL
        ''',
    ),
]
