SELECT
    date,
    region,
    series_label AS measure,
    value        AS load_mwh
FROM "bundesnetzagentur-consumption"
WHERE value IS NOT NULL
ORDER BY date, region, measure
