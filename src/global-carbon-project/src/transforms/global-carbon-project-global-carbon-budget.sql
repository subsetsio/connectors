SELECT CAST(year AS INTEGER) AS year,
       series,
       CAST(value AS DOUBLE) AS value
FROM "global-carbon-project-global-carbon-budget"
WHERE value IS NOT NULL
