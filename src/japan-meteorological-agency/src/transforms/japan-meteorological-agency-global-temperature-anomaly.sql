SELECT
    make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
    year, month, anomaly
FROM "japan-meteorological-agency-global-temperature-anomaly"
WHERE anomaly IS NOT NULL
ORDER BY year, month
