SELECT DISTINCT CAST(date AS DATE) AS date, region,
       CAST(hmi AS DOUBLE) AS hmi
FROM "nahb-hmi-regional-history" WHERE hmi IS NOT NULL
