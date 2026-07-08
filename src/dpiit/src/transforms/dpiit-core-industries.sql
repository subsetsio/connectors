SELECT
    sector,
    base_year,
    CAST(date AS DATE) AS date,
    CAST(index_value AS DOUBLE) AS index_value,
    CAST(growth_rate AS DOUBLE) AS growth_rate
FROM "dpiit-core-industries"
WHERE index_value IS NOT NULL
