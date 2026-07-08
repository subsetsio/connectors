SELECT variable, region, CAST(year AS INTEGER) AS year, period, CAST(value AS DOUBLE) AS value
FROM "dwd-regional-monthly"
WHERE value IS NOT NULL
