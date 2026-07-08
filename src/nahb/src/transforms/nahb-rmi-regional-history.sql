SELECT period, CAST(date AS DATE) AS date, region, measure,
       CAST(value AS DOUBLE) AS value
FROM "nahb-rmi-regional-history" WHERE value IS NOT NULL
