SELECT country,
       CAST(year AS INTEGER) AS year,
       CAST(value AS DOUBLE) AS value
FROM "global-carbon-project-national-fossil-consumption-emissions"
WHERE value IS NOT NULL
