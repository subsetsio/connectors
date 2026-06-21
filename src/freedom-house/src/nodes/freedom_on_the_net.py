"""Freedom on the Net — country score panel."""

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

_URL = "https://freedomhouse.org/sites/default/files/2023-09/FOTN_2023_Country_Score_Data.xlsx"

_FOTN_RENAME = {"Country": "country", "Edition": "year", "Status": "status", "Total": "total"}


def fetch_freedom_on_the_net(node_id: str) -> None:
    """Freedom on the Net country score panel — one row per country per edition
    year: total internet-freedom score (0-100), status, and the A/B/C
    subcategory sums plus their sub-indicators."""
    wb = _workbook(_URL)
    ws = _data_sheet(wb, exclude_substrings=_NOTES)
    rows = _sheet_rows(ws)
    h = _find_header_row(rows, "Country")
    header = [_txt(c) for c in rows[h]]
    keys = [_FOTN_RENAME.get(col, (col or "").strip().lower()) for col in header]
    out = []
    for raw in rows[h + 1:]:
        rec = {}
        for k, v in zip(keys, raw):
            if not k:
                continue
            if k == "year":
                rec[k] = _year(v)
            elif k in ("country", "status"):
                rec[k] = _txt(v)
            else:
                rec[k] = _num(v)
        if rec.get("country") and rec.get("year") is not None:
            out.append(rec)
    wb.close()
    save_raw_ndjson(out, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="freedom-house-freedom-on-the-net", fn=fetch_freedom_on_the_net, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="freedom-house-freedom-on-the-net-transform",
        deps=["freedom-house-freedom-on-the-net"],
        sql='''
            SELECT
                country,
                CAST(year AS INTEGER) AS year,
                status,
                a1, a2, a3, a4, a5, a,
                b1, b2, b3, b4, b5, b6, b7, b8, b,
                c1, c2, c3, c4, c5, c6, c7, c8, c,
                total
            FROM "freedom-house-freedom-on-the-net"
            WHERE country IS NOT NULL AND year IS NOT NULL
        ''',
    ),
]
