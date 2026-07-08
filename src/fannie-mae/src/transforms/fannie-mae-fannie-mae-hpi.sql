SELECT
    CAST(date AS DATE)        AS date,
    CAST(year AS INTEGER)     AS year,
    CAST(quarter AS INTEGER)  AS quarter,
    CAST(index_type AS VARCHAR) AS index_type,
    CAST(value AS DOUBLE)     AS value
FROM "fannie-mae-fannie-mae-hpi"
WHERE value IS NOT NULL
