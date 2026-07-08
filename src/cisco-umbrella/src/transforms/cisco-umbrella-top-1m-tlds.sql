SELECT
    CAST(rank AS INTEGER) AS rank,
    tld
FROM "cisco-umbrella-top-1m-tlds"
WHERE tld IS NOT NULL AND tld <> ''
ORDER BY rank
