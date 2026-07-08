SELECT city, state, CAST(year AS INTEGER) AS year, category,
       CAST(value AS DOUBLE) AS value
FROM "lincoln-institute-fisc-values"
WHERE value IS NOT NULL
