SELECT
    CAST(month AS DATE) AS month,
    country,
    gprc,
    gprhc
FROM "geopolitical-risk-index-gpr-country-monthly"
WHERE gprc IS NOT NULL OR gprhc IS NOT NULL
ORDER BY month, country
