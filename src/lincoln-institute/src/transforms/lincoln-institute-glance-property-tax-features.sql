SELECT state, CAST(year AS INTEGER) AS year, metric, value
FROM "lincoln-institute-glance-property-tax-features"
WHERE value IS NOT NULL
