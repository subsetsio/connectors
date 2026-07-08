SELECT
    chain,
    CAST(tvl AS DOUBLE)      AS tvl,
    token_symbol,
    gecko_id,
    CAST(cmc_id AS VARCHAR)  AS cmc_id,
    CAST(chain_id AS BIGINT) AS chain_id
FROM "defillama-chains"
WHERE chain IS NOT NULL
