"""DefiLlama dimension adapters — fees, dex volumes, options volumes.

A single parametric fetch over api.llama.fi/overview/{fees,dexs,options}; each
node_id selects its overview path but the payload shape, parse, and published
schema are identical, so all three subsets live in this one file.
"""
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import _get_json, _join_chains


_OVERVIEW_PATH = {
    "defillama-fees": "fees",
    "defillama-dex-volumes": "dexs",
    "defillama-options-volumes": "options",
}


def fetch_dimension(node_id: str) -> None:
    path = _OVERVIEW_PATH[node_id]
    url = (
        f"https://api.llama.fi/overview/{path}"
        "?excludeTotalDataChart=true&excludeTotalDataChartBreakdown=true"
    )
    payload = _get_json(url)
    data = payload.get("protocols", []) if isinstance(payload, dict) else payload
    rows = [{
        "protocol_id": p.get("defillamaId"),
        "name": p.get("name"),
        "display_name": p.get("displayName"),
        "slug": p.get("slug"),
        "category": p.get("category"),
        "protocol_type": p.get("protocolType"),
        "chains": _join_chains(p.get("chains")),
        "total_24h": p.get("total24h"),
        "total_7d": p.get("total7d"),
        "total_30d": p.get("total30d"),
        "total_1y": p.get("total1y"),
        "total_all_time": p.get("totalAllTime"),
        "average_1y": p.get("average1y"),
        "change_1d": p.get("change_1d"),
        "change_7d": p.get("change_7d"),
        "change_1m": p.get("change_1m"),
    } for p in data]
    save_raw_ndjson(rows, node_id)


_DIMENSION_SQL = '''
    SELECT
        CAST(protocol_id AS VARCHAR)  AS protocol_id,
        name,
        display_name,
        slug,
        category,
        protocol_type,
        chains,
        CAST(total_24h AS DOUBLE)     AS total_24h,
        CAST(total_7d AS DOUBLE)      AS total_7d,
        CAST(total_30d AS DOUBLE)     AS total_30d,
        CAST(total_1y AS DOUBLE)      AS total_1y,
        CAST(total_all_time AS DOUBLE) AS total_all_time,
        CAST(average_1y AS DOUBLE)    AS average_1y,
        CAST(change_1d AS DOUBLE)     AS change_1d,
        CAST(change_7d AS DOUBLE)     AS change_7d,
        CAST(change_1m AS DOUBLE)     AS change_1m
    FROM "{dep}"
    WHERE name IS NOT NULL
'''


DOWNLOAD_SPECS = [
    NodeSpec(id="defillama-fees", fn=fetch_dimension, kind="download"),
    NodeSpec(id="defillama-dex-volumes", fn=fetch_dimension, kind="download"),
    NodeSpec(id="defillama-options-volumes", fn=fetch_dimension, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="defillama-fees-transform",
        deps=["defillama-fees"],
        sql=_DIMENSION_SQL.format(dep="defillama-fees"),
    ),
    SqlNodeSpec(
        id="defillama-dex-volumes-transform",
        deps=["defillama-dex-volumes"],
        sql=_DIMENSION_SQL.format(dep="defillama-dex-volumes"),
    ),
    SqlNodeSpec(
        id="defillama-options-volumes-transform",
        deps=["defillama-options-volumes"],
        sql=_DIMENSION_SQL.format(dep="defillama-options-volumes"),
    ),
]
