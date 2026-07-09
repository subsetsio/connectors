SELECT
    CAST(date AS DATE) AS date,
    period,
    statistic,
    variable,
    block,
    CAST(value AS DOUBLE) AS value
FROM "kenneth-french-data-library-asia-pacific-ex-japan-6-portfolios-me-be-me"
WHERE value IS NOT NULL
