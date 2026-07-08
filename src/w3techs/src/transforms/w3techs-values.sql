SELECT
    category,
    category_name,
    technology,
    CAST(date AS DATE)        AS date,
    metric,
    CAST(percent AS DOUBLE)   AS percent
FROM "w3techs-values"
WHERE percent IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY category, technology, date, metric
    ORDER BY percent DESC
) = 1
