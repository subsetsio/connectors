"""Nasdaq ETF screener — full snapshot (stateless full re-pull)."""
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import _s, _etf_rows


def fetch_etfs(node_id: str) -> None:
    asset = node_id
    rows = _etf_rows()
    if len(rows) < 1000:
        raise RuntimeError(f"etf screener returned {len(rows)} rows; expected >=1000")
    out = [{
        "symbol": _s(r.get("symbol")),
        "companyName": _s(r.get("companyName")),
        "lastSalePrice": _s(r.get("lastSalePrice")),
        "netChange": _s(r.get("netChange")),
        "percentageChange": _s(r.get("percentageChange")),
        "oneYearPercentage": _s(r.get("oneYearPercentage")),
    } for r in rows]
    save_raw_ndjson(out, asset)


_NUM = "replace(replace(replace({c}, '$', ''), ',', ''), '%', '')"  # strip $ , %


DOWNLOAD_SPECS = [
    NodeSpec(id="nasdaq-etfs", fn=fetch_etfs, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nasdaq-etfs-transform",
        deps=["nasdaq-etfs"],
        sql=f'''
            SELECT
                symbol,
                companyName AS name,
                TRY_CAST({_NUM.format(c="lastSalePrice")} AS DOUBLE)     AS last_sale_price,
                TRY_CAST(replace({_NUM.format(c="netChange")}, '+', '') AS DOUBLE) AS net_change,
                TRY_CAST(replace({_NUM.format(c="percentageChange")}, '+', '') AS DOUBLE) AS pct_change,
                TRY_CAST(replace({_NUM.format(c="oneYearPercentage")}, '+', '') AS DOUBLE) AS one_year_pct_change
            FROM "nasdaq-etfs"
            WHERE symbol IS NOT NULL
        ''',
    ),
]
