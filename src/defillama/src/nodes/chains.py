"""DefiLlama chains — per-chain TVL snapshot (api.llama.fi/v2/chains)."""
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import _get_json


def fetch_chains(node_id: str) -> None:
    data = _get_json("https://api.llama.fi/v2/chains")
    rows = [{
        "chain": c.get("name"),
        "tvl": c.get("tvl"),
        "token_symbol": c.get("tokenSymbol"),
        "gecko_id": c.get("gecko_id"),
        "cmc_id": c.get("cmcId"),
        "chain_id": c.get("chainId"),
    } for c in data]
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="defillama-chains", fn=fetch_chains, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="defillama-chains-transform",
        deps=["defillama-chains"],
        sql='''
            SELECT
                chain,
                CAST(tvl AS DOUBLE)      AS tvl,
                token_symbol,
                gecko_id,
                CAST(cmc_id AS VARCHAR)  AS cmc_id,
                CAST(chain_id AS BIGINT) AS chain_id
            FROM "defillama-chains"
            WHERE chain IS NOT NULL
        ''',
    ),
]
