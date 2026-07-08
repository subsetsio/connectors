SELECT coin_id, date, price_usd, market_cap_usd, total_volume_usd
FROM (
    SELECT
        coin_id,
        CAST(to_timestamp(ts_ms / 1000.0) AS DATE) AS date,
        price_usd,
        market_cap_usd,
        total_volume_usd,
        row_number() OVER (
            PARTITION BY coin_id, CAST(to_timestamp(ts_ms / 1000.0) AS DATE)
            ORDER BY ts_ms DESC
        ) AS rn
    FROM "coingecko-coin-history"
    WHERE price_usd IS NOT NULL
)
WHERE rn = 1
