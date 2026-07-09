SELECT
    CAST(date AS DATE) AS date,
    period,
    statistic,
    variable,
    block,
    CAST(value AS DOUBLE) AS value
FROM "kenneth-french-data-library-north-america-25-portfolios-me-prior-250-20-daily"
WHERE value IS NOT NULL
