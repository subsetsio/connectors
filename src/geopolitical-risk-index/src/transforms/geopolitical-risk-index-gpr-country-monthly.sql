SELECT
    CAST(month AS DATE) AS month,
    CAST(country AS VARCHAR) AS country,
    CAST(gprc AS DOUBLE) AS gprc,
    CAST(gprhc AS DOUBLE) AS gprhc
FROM "geopolitical-risk-index-gpr-country-monthly"
WHERE gprc IS NOT NULL OR gprhc IS NOT NULL
