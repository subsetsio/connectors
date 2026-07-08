SELECT
    country,
    variable,
    percentile,
    CAST(year AS INTEGER)  AS year,
    CAST(value AS DOUBLE)  AS value,
    age,
    pop
FROM "world-inequality-database-values"
WHERE value IS NOT NULL
