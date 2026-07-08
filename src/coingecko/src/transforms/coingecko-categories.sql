SELECT
    id AS category_id,
    name,
    market_cap,
    market_cap_change_24h,
    volume_24h,
    top_3_coins,
    content,
    CAST(updated_at AS TIMESTAMP) AS updated_at
FROM "coingecko-categories"
WHERE id IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY id ORDER BY updated_at DESC) = 1
