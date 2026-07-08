SELECT
    variable,
    forecast_season,
    horizon,
    publication_round,
    unit,
    CAST(value AS DOUBLE) AS value
FROM "icac-published-forecasts"
WHERE value IS NOT NULL
