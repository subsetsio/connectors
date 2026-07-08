SELECT
    CAST(to_timestamp(CAST(date AS BIGINT)) AS DATE) AS date,
    CAST(tvl AS DOUBLE) AS tvl
FROM "defillama-historical-chain-tvl"
WHERE date IS NOT NULL
ORDER BY date
