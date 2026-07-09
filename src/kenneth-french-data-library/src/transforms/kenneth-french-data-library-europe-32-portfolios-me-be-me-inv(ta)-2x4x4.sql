SELECT
    CAST(date AS DATE) AS date,
    period,
    statistic,
    variable,
    block,
    CAST(value AS DOUBLE) AS value
FROM "kenneth-french-data-library-europe-32-portfolios-me-be-me-inv(ta)-2x4x4"
WHERE value IS NOT NULL
