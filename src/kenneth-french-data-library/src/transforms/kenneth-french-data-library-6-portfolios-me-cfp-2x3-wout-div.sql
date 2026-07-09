SELECT
    CAST(date AS DATE) AS date,
    period,
    statistic,
    variable,
    block,
    CAST(value AS DOUBLE) AS value
FROM "kenneth-french-data-library-6-portfolios-me-cfp-2x3-wout-div"
WHERE value IS NOT NULL
