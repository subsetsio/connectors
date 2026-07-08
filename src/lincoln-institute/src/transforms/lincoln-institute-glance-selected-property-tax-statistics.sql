SELECT state, CAST(year AS INTEGER) AS year, metric,
       CAST(value AS DOUBLE) AS value
FROM "lincoln-institute-glance-selected-property-tax-statistics"
WHERE value IS NOT NULL
