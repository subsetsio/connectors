SELECT
    CAST(day AS DATE) AS date,
    os,
    version,
    CAST(downloads AS BIGINT) AS downloads
FROM "cran-logs-r-downloads"
WHERE day IS NOT NULL
  AND os IS NOT NULL
  AND version IS NOT NULL
  AND downloads IS NOT NULL
