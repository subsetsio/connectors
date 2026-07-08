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
