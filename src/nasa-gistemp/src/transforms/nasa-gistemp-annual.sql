SELECT
    CAST(year AS INTEGER) AS year,
    region,
    CAST(anomaly_c AS DOUBLE) AS anomaly_c
FROM "nasa-gistemp-annual"
WHERE anomaly_c IS NOT NULL
