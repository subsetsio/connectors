SELECT
    month_name,
    to_timestamp(start_of_month) AS start_of_month,
    CAST(rank AS INTEGER)        AS rank,
    CAST(appid AS BIGINT)        AS appid
FROM "steamdb-top-releases"
WHERE appid IS NOT NULL
ORDER BY start_of_month DESC, rank
