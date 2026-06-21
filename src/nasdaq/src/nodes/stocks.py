"""Nasdaq stocks screener — full snapshot (stateless full re-pull)."""
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import _s, _stock_rows


def fetch_stocks(node_id: str) -> None:
    asset = node_id
    rows = _stock_rows()
    if len(rows) < 3000:
        raise RuntimeError(f"stocks screener returned {len(rows)} rows; expected >=3000")
    out = [{
        "symbol": _s(r.get("symbol")),
        "name": _s(r.get("name")),
        "lastsale": _s(r.get("lastsale")),
        "netchange": _s(r.get("netchange")),
        "pctchange": _s(r.get("pctchange")),
        "marketCap": _s(r.get("marketCap")),
    } for r in rows]
    save_raw_ndjson(out, asset)


_NUM = "replace(replace(replace({c}, '$', ''), ',', ''), '%', '')"  # strip $ , %


DOWNLOAD_SPECS = [
    NodeSpec(id="nasdaq-stocks", fn=fetch_stocks, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nasdaq-stocks-transform",
        deps=["nasdaq-stocks"],
        sql=f'''
            SELECT
                symbol,
                name,
                TRY_CAST({_NUM.format(c="lastsale")} AS DOUBLE)  AS last_sale,
                TRY_CAST({_NUM.format(c="netchange")} AS DOUBLE) AS net_change,
                TRY_CAST({_NUM.format(c="pctchange")} AS DOUBLE) AS pct_change,
                TRY_CAST({_NUM.format(c="marketCap")} AS DOUBLE) AS market_cap
            FROM "nasdaq-stocks"
            WHERE symbol IS NOT NULL
        ''',
    ),
]
