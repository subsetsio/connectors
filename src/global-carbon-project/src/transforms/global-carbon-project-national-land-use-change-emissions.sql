SELECT model,
       country,
       CAST(year AS INTEGER) AS year,
       CAST(value AS DOUBLE) AS value
FROM "global-carbon-project-national-land-use-change-emissions"
WHERE value IS NOT NULL
