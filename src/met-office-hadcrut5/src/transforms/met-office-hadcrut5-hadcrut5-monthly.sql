SELECT DISTINCT
    CAST(month AS VARCHAR)      AS month,
    CAST(region AS VARCHAR)     AS region,
    CAST(anomaly_c AS DOUBLE)   AS anomaly_c,
    CAST(lower_95_c AS DOUBLE)  AS lower_95_c,
    CAST(upper_95_c AS DOUBLE)  AS upper_95_c
FROM "met-office-hadcrut5-hadcrut5-monthly"
WHERE month IS NOT NULL AND anomaly_c IS NOT NULL
ORDER BY region, month
