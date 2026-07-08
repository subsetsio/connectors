SELECT
    CAST(month AS DATE) AS month,
    * EXCLUDE (month)
FROM "geopolitical-risk-index-gpr-monthly"
WHERE gpr IS NOT NULL OR gprh IS NOT NULL
ORDER BY month
