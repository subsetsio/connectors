SELECT
    CAST(appid AS BIGINT)                  AS appid,
    name,
    type,
    is_free,
    CAST(price_final_cents AS BIGINT)      AS price_final_cents,
    CAST(price_initial_cents AS BIGINT)    AS price_initial_cents,
    price_currency,
    CAST(discount_percent AS INTEGER)      AS discount_percent,
    genres,
    categories,
    on_windows,
    on_mac,
    on_linux,
    release_date,
    coming_soon,
    CAST(metacritic_score AS INTEGER)      AS metacritic_score,
    CAST(recommendations_total AS BIGINT)  AS recommendations_total
FROM "steamdb-app-details"
WHERE appid IS NOT NULL
