SELECT
    CAST(date AS DATE) AS date,
    * EXCLUDE (date)
FROM "geopolitical-risk-index-gpr-daily"
WHERE gprd IS NOT NULL
ORDER BY date
