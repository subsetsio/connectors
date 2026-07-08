SELECT
    package,
    CAST(day AS DATE) AS date,
    CAST(downloads AS BIGINT) AS downloads
FROM "cran-logs-package-downloads"
WHERE package IS NOT NULL
  AND day IS NOT NULL
  AND downloads IS NOT NULL
