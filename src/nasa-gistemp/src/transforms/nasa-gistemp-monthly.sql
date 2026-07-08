SELECT
    month,
    region,
    CAST(anomaly_c AS DOUBLE) AS anomaly_c
FROM "nasa-gistemp-monthly"
WHERE anomaly_c IS NOT NULL
