-- GISTEMP v4 monthly means, stacked long at download (Global/NH/SH files).
-- '***' cells arrived as nulls; drop them — a null anomaly is a non-observation
-- (future months of the current year, one incomplete 1880 seasonal cell).
SELECT
    "region" AS region,
    "year" AS year,
    "period" AS period,
    "anomaly_c" AS anomaly_c
FROM "nasa-gistemp-monthly-anomalies"
WHERE "anomaly_c" IS NOT NULL
