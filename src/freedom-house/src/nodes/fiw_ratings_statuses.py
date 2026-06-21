"""Freedom in the World — long historical ratings series (1972-present)."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import _num, _sheet_rows, _txt, _workbook, _year

_URL = "https://freedomhouse.org/sites/default/files/2025-02/Country_and_Territory_Ratings_and_Statuses_FIW_1973-2024.xlsx"


def fetch_fiw_ratings_statuses(node_id: str) -> None:
    """Freedom in the World long historical ratings series (1972-present). The
    workbook is WIDE — each survey edition occupies a 3-column block
    (PR, CL, Status) and the year sits in the 'Year(s) Under Review' row. We
    unpivot the Country and Territory sheets into long
    (entity_kind, country, year, pr, cl, status) rows."""
    wb = _workbook(_URL)
    out = []
    for sn in wb.sheetnames:
        low = sn.lower()
        if "ratings" not in low:
            continue
        kind = "territory" if "territor" in low else "country"
        rows = _sheet_rows(wb[sn])
        # locate the 'Year(s) Under Review' row and the PR/CL/Status sub-row.
        year_row = next(
            (r for r in rows[:6] if r and _txt(r[0]) and "year" in _txt(r[0]).lower()),
            None,
        )
        sub_row = next(
            (i for i, r in enumerate(rows[:6])
             if r and any(_txt(c) == "PR" for c in r[1:6])),
            None,
        )
        if year_row is None or sub_row is None:
            continue
        ncols = len(year_row)
        for raw in rows[sub_row + 1:]:
            country = _txt(raw[0]) if raw else None
            if not country:
                continue
            # each block: col=PR, col+1=CL, col+2=Status; year at year_row[col].
            for col in range(1, ncols - 2, 3):
                yr = _year(year_row[col])
                if yr is None:
                    continue
                pr = _num(raw[col]) if col < len(raw) else None
                cl = _num(raw[col + 1]) if col + 1 < len(raw) else None
                status = _txt(raw[col + 2]) if col + 2 < len(raw) else None
                if pr is None and cl is None and status is None:
                    continue
                out.append({
                    "entity_kind": kind,
                    "country": country,
                    "year": yr,
                    "pr": pr,
                    "cl": cl,
                    "status": status,
                })
    wb.close()
    save_raw_ndjson(out, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="freedom-house-fiw-ratings-statuses", fn=fetch_fiw_ratings_statuses, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="freedom-house-fiw-ratings-statuses-transform",
        deps=["freedom-house-fiw-ratings-statuses"],
        sql='''
            SELECT
                entity_kind,
                country,
                CAST(year AS INTEGER) AS year,
                CAST(pr AS INTEGER) AS pr,
                CAST(cl AS INTEGER) AS cl,
                status
            FROM "freedom-house-fiw-ratings-statuses"
            WHERE country IS NOT NULL AND year IS NOT NULL
              AND (pr IS NOT NULL OR cl IS NOT NULL OR status IS NOT NULL)
        ''',
    ),
]
