SELECT
    cube_id,
    series_key,
    series_label,
    frequency,
    unit,
    scale,
    period,
    CAST(value AS DOUBLE) AS value
FROM "swiss-national-bank-devwkibiim"
WHERE value IS NOT NULL
