SELECT
    CAST(rank AS INTEGER) AS rank,
    domain
FROM "cisco-umbrella-top-1m-domains"
WHERE domain IS NOT NULL AND domain <> ''
ORDER BY rank
