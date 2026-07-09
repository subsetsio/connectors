SELECT
    CAST(date AS DATE) AS date,
    period,
    statistic,
    variable,
    block,
    CAST(value AS DOUBLE) AS value
FROM "kenneth-french-data-library-100-portfolios-10x10-me-inv-wout-div"
WHERE value IS NOT NULL
