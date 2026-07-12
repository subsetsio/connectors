SELECT
    CAST(rank AS INTEGER) AS rank,
    CAST(domain AS VARCHAR) AS domain
FROM "cisco-umbrella-top-1m-domains"
WHERE domain IS NOT NULL AND domain <> ''
