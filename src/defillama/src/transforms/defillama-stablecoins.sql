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
