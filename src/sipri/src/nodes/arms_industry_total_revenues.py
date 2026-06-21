"""SIPRI arms industry total revenues — aggregate yearly total arms sales of the
Top 100, parsed from the Total-arms-revenues .xlsx. Stateless full re-pull
(SIPRI revises prior years on every annual release).
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import find_xlsx, isnum, load_wb

_TOTALREV_SCHEMA = pa.schema([
    ("year", pa.int32()),
    ("total_arms_revenue_current_usd_bn", pa.float64()),
])


def fetch_arms_industry_total_revenues(node_id: str) -> None:
    asset = node_id
    url = find_xlsx("/databases/armsindustry", "Total-arms-revenues")
    wb = load_wb(url)
    ws = wb[wb.sheetnames[0]]
    rows = list(ws.iter_rows(values_only=True))
    year_row = next(
        (r for r in rows if sum(1 for c in r if isnum(c) and 1990 < int(c) < 2100) > 3),
        None,
    )
    if year_row is None:
        raise RuntimeError("Total-arms-revenues: no year header row found")
    year_cols = {j: int(c) for j, c in enumerate(year_row) if isnum(c) and 1990 < int(c) < 2100}
    cur_row = next(
        (r for r in rows if isinstance(r[0], str) and "current US$" in r[0]),
        None,
    )
    if cur_row is None:
        raise RuntimeError("Total-arms-revenues: no 'current US$' value row found")
    out = [
        {"year": yr, "total_arms_revenue_current_usd_bn": float(cur_row[j])}
        for j, yr in year_cols.items()
        if j < len(cur_row) and isnum(cur_row[j])
    ]
    if not out:
        raise RuntimeError("arms-industry-total-revenues parse produced 0 rows")
    save_raw_parquet(pa.Table.from_pylist(out, schema=_TOTALREV_SCHEMA), asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="sipri-arms-industry-total-revenues", fn=fetch_arms_industry_total_revenues, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="sipri-arms-industry-total-revenues-transform",
        deps=["sipri-arms-industry-total-revenues"],
        sql='''
            SELECT
                CAST(year AS INTEGER) AS year,
                CAST(total_arms_revenue_current_usd_bn AS DOUBLE) AS total_arms_revenue_current_usd_bn
            FROM "sipri-arms-industry-total-revenues"
            WHERE total_arms_revenue_current_usd_bn IS NOT NULL
        ''',
    ),
]
