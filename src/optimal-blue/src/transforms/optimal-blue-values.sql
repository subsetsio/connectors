SELECT DISTINCT
    index_name,
    CAST(date AS DATE)   AS date,
    CAST(rate AS DOUBLE) AS rate
FROM "optimal-blue-values"
WHERE rate IS NOT NULL
