SELECT state, CAST(year AS INTEGER) AS year, metric,
       CAST(value AS DOUBLE) AS value
FROM "lincoln-institute-glance-sources-of-local-general-revenue"
WHERE value IS NOT NULL
