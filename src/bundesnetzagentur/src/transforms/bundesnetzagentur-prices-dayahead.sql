SELECT
    CAST(epoch_ms(date_ms + 43200000) AS DATE) AS date,
    series_label AS bidding_zone,
    value        AS price_eur_mwh
FROM "bundesnetzagentur-prices-dayahead"
WHERE value IS NOT NULL
ORDER BY date, bidding_zone
