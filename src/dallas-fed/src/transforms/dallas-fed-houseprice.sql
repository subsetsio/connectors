SELECT DISTINCT
    CAST(date AS DATE)      AS date,
    CAST(metric AS VARCHAR) AS metric,
    CAST(country AS VARCHAR) AS country,
    CAST(value AS DOUBLE)   AS value
FROM "dallas-fed-houseprice"
WHERE date IS NOT NULL AND value IS NOT NULL
