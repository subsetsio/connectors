"""DefiLlama protocols — full TVL protocol table (api.llama.fi/protocols)."""
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import _get_json, _join_chains


def fetch_protocols(node_id: str) -> None:
    data = _get_json("https://api.llama.fi/protocols")
    rows = [{
        "protocol_id": p.get("id"),
        "name": p.get("name"),
        "slug": p.get("slug"),
        "symbol": p.get("symbol"),
        "category": p.get("category"),
        "chain": p.get("chain"),
        "chains": _join_chains(p.get("chains")),
        "url": p.get("url"),
        "tvl": p.get("tvl"),
        "change_1h": p.get("change_1h"),
        "change_1d": p.get("change_1d"),
        "change_7d": p.get("change_7d"),
        "mcap": p.get("mcap"),
        "gecko_id": p.get("gecko_id"),
        "cmc_id": p.get("cmcId"),
        "twitter": p.get("twitter"),
        "listed_at": p.get("listedAt"),
    } for p in data]
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="defillama-protocols", fn=fetch_protocols, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="defillama-protocols-transform",
        deps=["defillama-protocols"],
        sql='''
            SELECT
                CAST(protocol_id AS VARCHAR) AS protocol_id,
                name,
                slug,
                symbol,
                category,
                chain,
                chains,
                url,
                CAST(tvl AS DOUBLE)        AS tvl,
                CAST(change_1h AS DOUBLE)  AS change_1h,
                CAST(change_1d AS DOUBLE)  AS change_1d,
                CAST(change_7d AS DOUBLE)  AS change_7d,
                CAST(mcap AS DOUBLE)       AS mcap,
                gecko_id,
                CAST(cmc_id AS VARCHAR)    AS cmc_id,
                twitter,
                CAST(to_timestamp(CAST(listed_at AS BIGINT)) AS TIMESTAMP) AS listed_at
            FROM "defillama-protocols"
            WHERE name IS NOT NULL
        ''',
    ),
]
