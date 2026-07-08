SELECT
    CAST(year AS INTEGER) AS year,
    zone,
    CAST(anomaly_c AS DOUBLE) AS anomaly_c
FROM "nasa-gistemp-zonal-annual"
WHERE anomaly_c IS NOT NULL
