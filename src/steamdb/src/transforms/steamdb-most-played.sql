SELECT
    CAST(rank AS INTEGER)            AS rank,
    CAST(appid AS BIGINT)            AS appid,
    CAST(last_week_rank AS INTEGER)  AS last_week_rank,
    CAST(peak_in_game AS BIGINT)     AS peak_in_game,
    CAST(rollup_date AS TIMESTAMPTZ) AS rollup_date
FROM "steamdb-most-played"
WHERE appid IS NOT NULL
ORDER BY rank
