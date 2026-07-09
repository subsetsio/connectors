SELECT
    region,
    month,
    CAST(absolute_temperature_c AS DOUBLE) AS absolute_temperature_c,
    CAST(anomaly_from_annual_mean_c AS DOUBLE) AS anomaly_from_annual_mean_c,
    CAST(annual_absolute_temperature_c AS DOUBLE) AS annual_absolute_temperature_c
FROM "climatic-research-unit-absolute-temperatures"
