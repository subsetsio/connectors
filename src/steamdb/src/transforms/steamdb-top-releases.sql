SELECT
    month_name,
    CAST(start_of_month AS TIMESTAMPTZ) AS start_of_month,
    CAST(rank AS INTEGER)        AS rank,
    CAST(appid AS BIGINT)        AS appid
FROM "steamdb-top-releases"
WHERE appid IS NOT NULL
ORDER BY start_of_month DESC, rank
