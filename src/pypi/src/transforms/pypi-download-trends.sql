SELECT
    package,
    category,
    CAST(date AS DATE)        AS date,
    CAST(downloads AS BIGINT) AS downloads
FROM "pypi-download-trends"
WHERE package IS NOT NULL
  AND date IS NOT NULL
  AND downloads IS NOT NULL
