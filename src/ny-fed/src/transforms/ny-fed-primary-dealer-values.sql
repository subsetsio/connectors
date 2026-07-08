SELECT
    TRY_CAST(asofdate AS DATE)           AS week_ending,
    keyid                                AS series_id,
    seriesbreak                          AS series_break,
    description                          AS series_description,
    TRY_CAST(value AS DOUBLE)            AS value_millions
FROM "ny-fed-primary-dealer-values"
WHERE TRY_CAST(asofdate AS DATE) IS NOT NULL
  AND TRY_CAST(value AS DOUBLE) IS NOT NULL
