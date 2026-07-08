SELECT
    CAST(market_id AS VARCHAR)                        AS market_id,
    CAST(timestamp AS BIGINT)                         AS timestamp,
    CAST(to_timestamp(timestamp) AS TIMESTAMP)       AS datetime,
    CAST(price AS DOUBLE)                            AS price
FROM (
    SELECT
        market_id, timestamp, price,
        row_number() OVER (
            PARTITION BY market_id, timestamp ORDER BY price
        ) AS _rn
    FROM "polymarket-price-history"
    WHERE market_id IS NOT NULL
      AND timestamp IS NOT NULL
      AND price IS NOT NULL
)
WHERE _rn = 1
