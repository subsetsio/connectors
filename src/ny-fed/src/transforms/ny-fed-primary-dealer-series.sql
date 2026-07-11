SELECT DISTINCT
    keyid                                AS series_id,
    seriesbreak                          AS series_break,
    description                          AS series_description
FROM "ny-fed-primary-dealer-series"
WHERE keyid IS NOT NULL AND keyid <> ''
