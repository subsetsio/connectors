SELECT CAST(year AS INTEGER) AS year,
       series,
       CAST(value AS DOUBLE) AS value
FROM "global-carbon-project-ocean-sink"
WHERE value IS NOT NULL
