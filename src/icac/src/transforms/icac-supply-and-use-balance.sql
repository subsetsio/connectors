SELECT
    country,
    season,
    CAST(year_begin AS INTEGER) AS year_begin,
    metric,
    unit,
    CAST(value AS DOUBLE) AS value
FROM "icac-supply-and-use-balance"
WHERE value IS NOT NULL
