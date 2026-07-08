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
