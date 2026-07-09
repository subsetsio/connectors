SELECT
    CAST(date AS DATE) AS date,
    period,
    statistic,
    variable,
    block,
    CAST(value AS DOUBLE) AS value
FROM "kenneth-french-data-library-europe-25-portfolios-me-be-me-daily"
WHERE value IS NOT NULL
