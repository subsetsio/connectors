SELECT period, CAST(date AS DATE) AS date, indicator,
       CAST(value AS DOUBLE) AS value
FROM "nahb-rmi-national-history" WHERE value IS NOT NULL
