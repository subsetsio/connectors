"""National Housing Survey monthly key indicators (no auth)."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import _ffill, _isodate, _load_rows, _num

# data-and-insights page slug + constant filename prefix.
_PAGE = ("national-housing-survey", "nhs-monthly-indicator-data")


def fetch_nhs(node_id: str) -> None:
    """National Housing Survey monthly key indicators. Two header rows:
    row 0 = section group (merged), row 1 = indicator; col 0 = month date.
    A trailing non-date footer block is skipped. Emit long format."""
    _, rows = _load_rows(node_id, *_PAGE)
    ncols = max((len(r) for r in rows[:3]), default=0)
    groups = _ffill(rows[0], ncols)
    subs = [None] * ncols
    for i in range(ncols):
        v = rows[1][i] if i < len(rows[1]) else None
        subs[i] = str(v).strip() if v is not None and str(v).strip() else None
    out = []
    for r in rows[2:]:
        date = _isodate(r[0])
        if date is None:  # footer / blank rows have a non-date in col 0
            continue
        for c in range(1, ncols):
            ind = subs[c]
            if not ind:
                continue
            val = _num(r[c]) if c < len(r) else None
            if val is None:
                continue
            out.append({
                "date": date,
                "category": groups[c],
                "indicator": ind,
                "value": val,
            })
    if not out:
        raise AssertionError(f"{node_id}: parsed 0 NHS rows")
    save_raw_ndjson(out, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="fannie-mae-nhs-monthly-indicator-data", fn=fetch_nhs, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fannie-mae-nhs-monthly-indicator-data-transform",
        deps=["fannie-mae-nhs-monthly-indicator-data"],
        sql='''
            SELECT
                CAST(date AS DATE)        AS date,
                CAST(category AS VARCHAR) AS category,
                CAST(indicator AS VARCHAR) AS indicator,
                CAST(value AS DOUBLE)     AS value
            FROM "fannie-mae-nhs-monthly-indicator-data"
            WHERE value IS NOT NULL
        ''',
    ),
]
