SELECT DISTINCT
    CAST(year AS VARCHAR)       AS year,
    CAST(region AS VARCHAR)     AS region,
    CAST(anomaly_c AS DOUBLE)   AS anomaly_c,
    CAST(lower_95_c AS DOUBLE)  AS lower_95_c,
    CAST(upper_95_c AS DOUBLE)  AS upper_95_c
FROM "met-office-hadcrut5-hadcrut5-annual"
WHERE year IS NOT NULL AND anomaly_c IS NOT NULL
ORDER BY region, year
