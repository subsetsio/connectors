SELECT DISTINCT CAST(date AS DATE) AS date, component,
       CAST(value AS DOUBLE) AS value
FROM "nahb-hmi-components-history" WHERE value IS NOT NULL
