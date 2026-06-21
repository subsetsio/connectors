"""DefiLlama historical chain TVL — aggregate total DeFi TVL daily series.

Aggregate total DeFi TVL across all chains, daily series back to 2017
(api.llama.fi/v2/historicalChainTvl).
"""
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import _get_json


def fetch_historical_chain_tvl(node_id: str) -> None:
    data = _get_json("https://api.llama.fi/v2/historicalChainTvl")
    rows = [{"date": d.get("date"), "tvl": d.get("tvl")} for d in data]
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="defillama-historical-chain-tvl", fn=fetch_historical_chain_tvl, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="defillama-historical-chain-tvl-transform",
        deps=["defillama-historical-chain-tvl"],
        sql='''
            SELECT
                CAST(to_timestamp(CAST(date AS BIGINT)) AS DATE) AS date,
                CAST(tvl AS DOUBLE) AS tvl
            FROM "defillama-historical-chain-tvl"
            WHERE date IS NOT NULL
            ORDER BY date
        ''',
    ),
]
