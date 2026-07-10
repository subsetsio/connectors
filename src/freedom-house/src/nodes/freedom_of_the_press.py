"""Freedom of the Press — historical panel (1980-2017, report discontinued)."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import _data_sheet, _num, _sheet_rows, _txt, _workbook, _year

_URL = "https://freedomhouse.org/sites/default/files/2020-02/FOTP1980-FOTP2017_Public-Data.xlsx"

_FOTP_FIELD = {
    "Total Score": "total_score",
    "Status": "status",
    "A-Legal": "legal",
    "B-Political": "political",
    "C-Economic": "economic",
}


def fetch_freedom_of_the_press(node_id: str) -> None:
    """Freedom of the Press historical panel (1980-2017, report discontinued).
    The 'Data' sheet is WIDE with era-varying column layouts; the edition year
    sits in the 'Press Freedom Edition' row (forward-filled across each block)
    and the comparable per-edition fields (Total Score, Status, and the
    Legal/Political/Economic subscores present from 2002) live in the subheader
    row. We unpivot to long (country, year, total_score, status, legal,
    political, economic)."""
    wb = _workbook(_URL)
    ws = _data_sheet(wb, exclude_substrings=("intro", "legend", "key", "notes"))
    rows = _sheet_rows(ws)
    # find the edition row and the subheader row.
    edition_row = next(
        (r for r in rows[:8] if r and _txt(r[0]) and "edition" in _txt(r[0]).lower()),
        None,
    )
    sub_idx = next(
        (i for i, r in enumerate(rows[:10])
         if r and any(_txt(c) in _FOTP_FIELD for c in r[1:])),
        None,
    )
    assert edition_row is not None and sub_idx is not None, "FOTP: header rows not found"
    ncols = len(edition_row)
    # forward-fill the edition year across each block (merged cells read as None).
    col_year = [None] * ncols
    cur = None
    for c in range(1, ncols):
        y = _year(edition_row[c])
        if y is not None:
            cur = y
        col_year[c] = cur
    sub_row = [_txt(c) for c in rows[sub_idx]]
    col_field = [
        _FOTP_FIELD.get(sub_row[c]) if c < len(sub_row) else None
        for c in range(ncols)
    ]
    out = []
    for raw in rows[sub_idx + 1:]:
        country = _txt(raw[0]) if raw else None
        if not country:
            continue
        per_year: dict[int, dict] = {}
        for c in range(1, ncols):
            field = col_field[c]
            yr = col_year[c]
            if not field or yr is None or c >= len(raw):
                continue
            val = _txt(raw[c]) if field == "status" else _num(raw[c])
            if val is None:
                continue
            per_year.setdefault(yr, {})[field] = val
        for yr, fields in per_year.items():
            out.append({
                "country": country,
                "year": yr,
                "total_score": fields.get("total_score"),
                "status": fields.get("status"),
                "legal": fields.get("legal"),
                "political": fields.get("political"),
                "economic": fields.get("economic"),
            })
    wb.close()
    save_raw_ndjson(out, node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="freedom-house-freedom-of-the-press", fn=fetch_freedom_of_the_press, kind="download"),
]

_TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="freedom-house-freedom-of-the-press-transform",
        deps=["freedom-house-freedom-of-the-press"],
        sql='''
            SELECT
                country,
                CAST(year AS INTEGER) AS year,
                total_score,
                status,
                legal,
                political,
                economic
            FROM "freedom-house-freedom-of-the-press"
            WHERE country IS NOT NULL AND year IS NOT NULL
              AND (total_score IS NOT NULL OR status IS NOT NULL)
        ''',
    ),
]
