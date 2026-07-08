SELECT
    CAST(date AS DATE) AS date,
    period,
    statistic,
    variable,
    block,
    CAST(value AS DOUBLE) AS value
FROM "kenneth-french-data-library-north-america-6-portfolios-me-prior-12-2"
WHERE value IS NOT NULL
