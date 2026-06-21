"""DefiLlama stablecoins — circulating supply per pegged asset.

stablecoins.llama.fi/stablecoins?includePrices=true
"""
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import _get_json


def _circ(d, peg_type):
    """circulating fields are {pegType: amount}; extract the amount for this peg."""
    if isinstance(d, dict):
        if peg_type in d:
            return d[peg_type]
        # fall back to the sole value if the peg key isn't present
        vals = [v for v in d.values() if isinstance(v, (int, float))]
        return vals[0] if len(vals) == 1 else None
    return None


def fetch_stablecoins(node_id: str) -> None:
    payload = _get_json("https://stablecoins.llama.fi/stablecoins?includePrices=true")
    assets = payload.get("peggedAssets", []) if isinstance(payload, dict) else payload
    rows = []
    for a in assets:
        peg = a.get("pegType")
        rows.append({
            "stablecoin_id": a.get("id"),
            "name": a.get("name"),
            "symbol": a.get("symbol"),
            "gecko_id": a.get("gecko_id"),
            "peg_type": peg,
            "peg_mechanism": a.get("pegMechanism"),
            "price": a.get("price"),
            "circulating": _circ(a.get("circulating"), peg),
            "circulating_prev_day": _circ(a.get("circulatingPrevDay"), peg),
            "circulating_prev_week": _circ(a.get("circulatingPrevWeek"), peg),
            "circulating_prev_month": _circ(a.get("circulatingPrevMonth"), peg),
        })
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="defillama-stablecoins", fn=fetch_stablecoins, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="defillama-stablecoins-transform",
        deps=["defillama-stablecoins"],
        sql='''
            SELECT
                CAST(stablecoin_id AS VARCHAR) AS stablecoin_id,
                name,
                symbol,
                gecko_id,
                peg_type,
                peg_mechanism,
                CAST(price AS DOUBLE)        AS price,
                CAST(circulating AS DOUBLE)  AS circulating,
                CAST(circulating_prev_day AS DOUBLE)   AS circulating_prev_day,
                CAST(circulating_prev_week AS DOUBLE)  AS circulating_prev_week,
                CAST(circulating_prev_month AS DOUBLE) AS circulating_prev_month
            FROM "defillama-stablecoins"
            WHERE stablecoin_id IS NOT NULL
        ''',
    ),
]
