"""DefiLlama yield pools — APY/TVL per pool (yields.llama.fi/pools)."""
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import _get_json


def fetch_yield_pools(node_id: str) -> None:
    payload = _get_json("https://yields.llama.fi/pools")
    data = payload.get("data", []) if isinstance(payload, dict) else payload
    rows = [{
        "pool_id": p.get("pool"),
        "chain": p.get("chain"),
        "project": p.get("project"),
        "symbol": p.get("symbol"),
        "pool_meta": p.get("poolMeta"),
        "tvl_usd": p.get("tvlUsd"),
        "apy": p.get("apy"),
        "apy_base": p.get("apyBase"),
        "apy_reward": p.get("apyReward"),
        "apy_mean_30d": p.get("apyMean30d"),
        "apy_pct_1d": p.get("apyPct1D"),
        "apy_pct_7d": p.get("apyPct7D"),
        "apy_pct_30d": p.get("apyPct30D"),
        "stablecoin": p.get("stablecoin"),
        "il_risk": p.get("ilRisk"),
        "exposure": p.get("exposure"),
        "count": p.get("count"),
        "volume_usd_1d": p.get("volumeUsd1d"),
        "volume_usd_7d": p.get("volumeUsd7d"),
    } for p in data]
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="defillama-yield-pools", fn=fetch_yield_pools, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="defillama-yield-pools-transform",
        deps=["defillama-yield-pools"],
        sql='''
            SELECT
                CAST(pool_id AS VARCHAR) AS pool_id,
                chain,
                project,
                symbol,
                pool_meta,
                CAST(tvl_usd AS DOUBLE)      AS tvl_usd,
                CAST(apy AS DOUBLE)          AS apy,
                CAST(apy_base AS DOUBLE)     AS apy_base,
                CAST(apy_reward AS DOUBLE)   AS apy_reward,
                CAST(apy_mean_30d AS DOUBLE) AS apy_mean_30d,
                CAST(apy_pct_1d AS DOUBLE)   AS apy_pct_1d,
                CAST(apy_pct_7d AS DOUBLE)   AS apy_pct_7d,
                CAST(apy_pct_30d AS DOUBLE)  AS apy_pct_30d,
                stablecoin,
                il_risk,
                exposure,
                CAST(count AS BIGINT)        AS pool_count,
                CAST(volume_usd_1d AS DOUBLE) AS volume_usd_1d,
                CAST(volume_usd_7d AS DOUBLE) AS volume_usd_7d
            FROM "defillama-yield-pools"
            WHERE pool_id IS NOT NULL
        ''',
    ),
]
