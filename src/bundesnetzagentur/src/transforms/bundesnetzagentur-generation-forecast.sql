SELECT
    CAST(epoch_ms(date_ms + 43200000) AS DATE) AS date,
    region,
    series_label AS source,
    value        AS forecast_mwh
FROM "bundesnetzagentur-generation-forecast"
WHERE value IS NOT NULL
ORDER BY date, region, source
