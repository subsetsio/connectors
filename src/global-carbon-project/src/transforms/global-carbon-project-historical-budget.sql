SELECT CAST(year AS INTEGER) AS year,
       series,
       CAST(value AS DOUBLE) AS value
FROM "global-carbon-project-historical-budget"
WHERE value IS NOT NULL
