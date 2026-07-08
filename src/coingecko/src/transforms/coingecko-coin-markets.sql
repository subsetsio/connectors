SELECT
    id AS coin_id,
    symbol,
    name,
    current_price,
    market_cap,
    CAST(market_cap_rank AS BIGINT) AS market_cap_rank,
    fully_diluted_valuation,
    total_volume,
    high_24h,
    low_24h,
    price_change_24h,
    price_change_percentage_24h,
    market_cap_change_24h,
    market_cap_change_percentage_24h,
    circulating_supply,
    total_supply,
    max_supply,
    ath,
    ath_change_percentage,
    CAST(ath_date AS TIMESTAMP) AS ath_date,
    atl,
    atl_change_percentage,
    CAST(atl_date AS TIMESTAMP) AS atl_date,
    CAST(last_updated AS TIMESTAMP) AS last_updated
FROM "coingecko-coin-markets"
WHERE id IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY id ORDER BY last_updated DESC) = 1
