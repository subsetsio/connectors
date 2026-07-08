SELECT CAST(date AS DATE) AS date, CAST(hmi AS DOUBLE) AS hmi
FROM "nahb-hmi-national-history" WHERE hmi IS NOT NULL
