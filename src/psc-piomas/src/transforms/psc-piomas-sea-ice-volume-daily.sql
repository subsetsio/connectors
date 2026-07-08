SELECT
    CAST(date AS DATE)                AS date,
    CAST(volume_thousand_km3 AS DOUBLE) AS volume_thousand_km3
FROM "psc-piomas-sea-ice-volume-daily"
WHERE volume_thousand_km3 IS NOT NULL
ORDER BY date
