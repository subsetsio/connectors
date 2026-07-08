SELECT
    language,
    CAST(date AS DATE)         AS date,
    CAST(rating_pct AS DOUBLE) AS rating_pct
FROM "tiobe-historical-ratings"
WHERE rating_pct IS NOT NULL
