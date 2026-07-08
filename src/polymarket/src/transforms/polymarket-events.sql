SELECT * EXCLUDE (_rn) FROM (
    SELECT
        CAST(event_id AS VARCHAR)       AS event_id,
        CAST(ticker AS VARCHAR)         AS ticker,
        CAST(slug AS VARCHAR)           AS slug,
        CAST(title AS VARCHAR)          AS title,
        CAST(category AS VARCHAR)       AS category,
        CAST(description AS VARCHAR)    AS description,
        CAST(volume_usd AS DOUBLE)      AS volume_usd,
        CAST(volume_24h_usd AS DOUBLE)  AS volume_24h_usd,
        CAST(volume_1wk_usd AS DOUBLE)  AS volume_1wk_usd,
        CAST(volume_1mo_usd AS DOUBLE)  AS volume_1mo_usd,
        CAST(volume_1yr_usd AS DOUBLE)  AS volume_1yr_usd,
        CAST(liquidity_usd AS DOUBLE)   AS liquidity_usd,
        CAST(open_interest AS DOUBLE)   AS open_interest,
        CAST(comment_count AS BIGINT)   AS comment_count,
        CAST(competitive AS DOUBLE)     AS competitive,
        CAST(neg_risk AS BOOLEAN)       AS neg_risk,
        CAST(is_active AS BOOLEAN)      AS is_active,
        CAST(is_closed AS BOOLEAN)      AS is_closed,
        CAST(is_archived AS BOOLEAN)    AS is_archived,
        CAST(is_featured AS BOOLEAN)    AS is_featured,
        CAST(is_restricted AS BOOLEAN)  AS is_restricted,
        CAST(market_count AS BIGINT)    AS market_count,
        TRY_CAST(start_date AS DATE)    AS start_date,
        TRY_CAST(end_date AS DATE)      AS end_date,
        TRY_CAST(creation_date AS DATE) AS creation_date,
        TRY_CAST(created_at AS TIMESTAMP) AS created_at,
        TRY_CAST(updated_at AS TIMESTAMP) AS updated_at,
        row_number() OVER (
            PARTITION BY event_id ORDER BY updated_at DESC NULLS LAST
        ) AS _rn
    FROM "polymarket-events"
    WHERE event_id IS NOT NULL
)
WHERE _rn = 1
