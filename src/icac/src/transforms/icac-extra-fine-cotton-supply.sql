SELECT
    item,
    country,
    CAST(year_begin AS INTEGER) AS year_begin,
    season,
    CAST(value AS DOUBLE) AS value
FROM "icac-extra-fine-cotton-supply"
WHERE value IS NOT NULL
