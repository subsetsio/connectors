SELECT
    package,
    CAST(date AS DATE)        AS date,
    CAST(downloads AS BIGINT) AS downloads
FROM "npm-daily-downloads"
WHERE package IS NOT NULL AND date IS NOT NULL
