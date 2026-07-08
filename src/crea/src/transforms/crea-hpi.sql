SELECT
    CAST(date AS DATE)            AS date,
    geography,
    geography_name,
    level,
    housing_type,
    frequency,
    seasonally_adjusted,
    CAST(hpi_index AS DOUBLE)       AS hpi_index,
    CAST(benchmark_price AS DOUBLE) AS benchmark_price
FROM "crea-hpi"
WHERE hpi_index IS NOT NULL OR benchmark_price IS NOT NULL
