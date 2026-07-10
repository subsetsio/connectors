SELECT
    date,
    series_label AS bidding_zone,
    value        AS price_eur_mwh
FROM "bundesnetzagentur-prices-dayahead"
WHERE value IS NOT NULL
ORDER BY date, bidding_zone
