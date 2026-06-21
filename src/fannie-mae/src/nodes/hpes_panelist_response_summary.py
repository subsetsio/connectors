"""HPES panelist response summary (latest round) (no auth)."""

import re

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import _ffill, _isodate, _load_rows, _num

# data-and-insights page slug + constant filename prefix (HPES page hosts two).
_PAGE = ("home-price-expectations-survey-hpes", "hpes-panelist-response-summary")


def fetch_hpes_panelist(node_id: str) -> None:
    """HPES panelist response summary (latest round): one row per panelist
    with per-year forecasts under two metric blocks (annual estimate /
    cumulative). row 5 = metric group (merged), row 6 = header
    (Panelist, Title, Affiliation, Response Date, then forecast years).
    Melt the year columns to long format."""
    _, rows = _load_rows(node_id, *_PAGE)
    # locate the header row (the one containing 'Panelist')
    hdr_idx = None
    for i, r in enumerate(rows[:20]):
        if any(c is not None and str(c).strip().lower() == "panelist" for c in r):
            hdr_idx = i
            break
    if hdr_idx is None:
        raise AssertionError(f"{node_id}: could not locate 'Panelist' header row")
    hdr = rows[hdr_idx]
    ncols = len(hdr)
    metrics = _ffill(rows[hdr_idx - 1], ncols) if hdr_idx >= 1 else [None] * ncols
    # map header cells: identify the label columns and the year columns
    col_panelist = col_title = col_affil = col_date = None
    year_cols = []  # (col_index, year_int)
    for c in range(ncols):
        v = hdr[c]
        if v is None:
            continue
        s = str(v).strip()
        sl = s.lower()
        if sl == "panelist":
            col_panelist = c
        elif sl == "title":
            col_title = c
        elif sl == "affiliation":
            col_affil = c
        elif sl == "response date":
            col_date = c
        elif re.fullmatch(r"\d{4}", s):
            year_cols.append((c, int(s)))
    if col_panelist is None or not year_cols:
        raise AssertionError(f"{node_id}: header missing panelist/year columns")
    out = []
    for r in rows[hdr_idx + 1:]:
        name = r[col_panelist] if len(r) > col_panelist else None
        if name is None or not str(name).strip():
            continue
        title = r[col_title] if col_title is not None and len(r) > col_title else None
        affil = r[col_affil] if col_affil is not None and len(r) > col_affil else None
        rdate = _isodate(r[col_date]) if col_date is not None and len(r) > col_date else None
        for c, yr in year_cols:
            val = _num(r[c]) if c < len(r) else None
            if val is None:
                continue
            out.append({
                "panelist": str(name).strip(),
                "title": str(title).strip() if title is not None else None,
                "affiliation": str(affil).strip() if affil is not None else None,
                "response_date": rdate,
                "metric": metrics[c],
                "forecast_year": yr,
                "value": val,
            })
    if not out:
        raise AssertionError(f"{node_id}: parsed 0 HPES panelist rows")
    save_raw_ndjson(out, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="fannie-mae-hpes-panelist-response-summary", fn=fetch_hpes_panelist, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fannie-mae-hpes-panelist-response-summary-transform",
        deps=["fannie-mae-hpes-panelist-response-summary"],
        sql='''
            SELECT
                CAST(panelist AS VARCHAR)      AS panelist,
                CAST(title AS VARCHAR)         AS title,
                CAST(affiliation AS VARCHAR)   AS affiliation,
                CAST(response_date AS DATE)    AS response_date,
                CAST(metric AS VARCHAR)        AS metric,
                CAST(forecast_year AS INTEGER) AS forecast_year,
                CAST(value AS DOUBLE)          AS value
            FROM "fannie-mae-hpes-panelist-response-summary"
            WHERE value IS NOT NULL
        ''',
    ),
]
