SELECT
    region, measure,
    make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
    year, month, value
FROM "japan-meteorological-agency-enso-sst-indices"
WHERE value IS NOT NULL
ORDER BY region, measure, year, month
