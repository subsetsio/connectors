SELECT
    market,
    market_name,
    province,
    market_type,
    CAST(sort_order AS BIGINT) AS sort_order
FROM "teranet-markets"
