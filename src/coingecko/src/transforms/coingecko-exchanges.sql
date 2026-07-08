SELECT
    id AS exchange_id,
    name,
    year_established,
    country,
    has_trading_incentive,
    trust_score,
    trust_score_rank,
    trade_volume_24h_btc
FROM "coingecko-exchanges"
WHERE id IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY id ORDER BY trust_score_rank) = 1
