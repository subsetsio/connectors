SELECT
    date,
    region,
    series_label AS source,
    value        AS forecast_mwh
FROM "bundesnetzagentur-generation-forecast"
WHERE value IS NOT NULL
ORDER BY date, region, source
