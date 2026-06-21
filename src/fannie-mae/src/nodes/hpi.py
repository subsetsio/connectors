"""Fannie Mae Home Price Index (no auth)."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import _load_rows, _num

# data-and-insights page slug + constant filename prefix.
_PAGE = ("fannie-mae-home-price-index", "fannie-mae-hpi")


def fetch_hpi(node_id: str) -> None:
    """Fannie Mae Home Price Index. Clean sheet: header row 0 =
    year, quarter, hpi_nsa, hpi_sa; data follows. Emit long format."""
    _, rows = _load_rows(node_id, *_PAGE)
    out = []
    for r in rows[1:]:
        year = _num(r[0])
        quarter = _num(r[1])
        if year is None or quarter is None:
            continue
        y, q = int(year), int(quarter)
        date = f"{y}-{(q - 1) * 3 + 1:02d}-01"
        for idx, col in (("nsa", 2), ("sa", 3)):
            val = _num(r[col]) if len(r) > col else None
            if val is not None:
                out.append({
                    "date": date, "year": y, "quarter": q,
                    "index_type": idx, "value": val,
                })
    if not out:
        raise AssertionError(f"{node_id}: parsed 0 HPI rows")
    save_raw_ndjson(out, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="fannie-mae-fannie-mae-hpi", fn=fetch_hpi, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fannie-mae-fannie-mae-hpi-transform",
        deps=["fannie-mae-fannie-mae-hpi"],
        sql='''
            SELECT
                CAST(date AS DATE)        AS date,
                CAST(year AS INTEGER)     AS year,
                CAST(quarter AS INTEGER)  AS quarter,
                CAST(index_type AS VARCHAR) AS index_type,
                CAST(value AS DOUBLE)     AS value
            FROM "fannie-mae-fannie-mae-hpi"
            WHERE value IS NOT NULL
        ''',
    ),
]
