SELECT DISTINCT CAST(date AS DATE) AS date, region,
       CAST(hmi_3mo_ma AS DOUBLE) AS hmi_3mo_ma
FROM "nahb-hmi-regional-3mo-moving-average" WHERE hmi_3mo_ma IS NOT NULL
