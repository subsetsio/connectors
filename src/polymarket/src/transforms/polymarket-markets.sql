SELECT * EXCLUDE (_rn) FROM (
    SELECT
        CAST(market_id AS VARCHAR)        AS market_id,
        CAST(event_id AS VARCHAR)         AS event_id,
        CAST(event_slug AS VARCHAR)       AS event_slug,
        CAST(event_title AS VARCHAR)      AS event_title,
        CAST(neg_risk AS BOOLEAN)         AS neg_risk,
        CAST(question AS VARCHAR)         AS question,
        CAST(slug AS VARCHAR)             AS slug,
        CAST(condition_id AS VARCHAR)     AS condition_id,
        CAST(outcome_yes_price AS DOUBLE) AS outcome_yes_price,
        CAST(outcome_no_price AS DOUBLE)  AS outcome_no_price,
        CAST(volume_usd AS DOUBLE)        AS volume_usd,
        CAST(volume_24h_usd AS DOUBLE)    AS volume_24h_usd,
        CAST(volume_1wk_usd AS DOUBLE)    AS volume_1wk_usd,
        CAST(volume_1mo_usd AS DOUBLE)    AS volume_1mo_usd,
        CAST(volume_1yr_usd AS DOUBLE)    AS volume_1yr_usd,
        CAST(liquidity_usd AS DOUBLE)     AS liquidity_usd,
        CAST(last_trade_price AS DOUBLE)  AS last_trade_price,
        CAST(best_bid AS DOUBLE)          AS best_bid,
        CAST(best_ask AS DOUBLE)          AS best_ask,
        CAST(spread AS DOUBLE)            AS spread,
        CAST(competitive AS DOUBLE)       AS competitive,
        CAST(is_active AS BOOLEAN)        AS is_active,
        CAST(is_closed AS BOOLEAN)        AS is_closed,
        TRY_CAST(start_date AS DATE)      AS start_date,
        TRY_CAST(end_date AS DATE)        AS end_date,
        TRY_CAST(created_at AS TIMESTAMP) AS created_at,
        TRY_CAST(updated_at AS TIMESTAMP) AS updated_at,
        row_number() OVER (
            PARTITION BY market_id ORDER BY updated_at DESC NULLS LAST
        ) AS _rn
    FROM "polymarket-markets"
    WHERE market_id IS NOT NULL
)
WHERE _rn = 1
