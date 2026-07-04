-- GISTEMP v4 zonal annual means, stacked long at download (ZonAnn file).
SELECT
    "year" AS year,
    "zone" AS zone,
    "anomaly_c" AS anomaly_c
FROM "nasa-gistemp-zonal-annual"
WHERE "anomaly_c" IS NOT NULL
