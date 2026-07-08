SELECT
    CAST(date AS DATE) AS date,
    period,
    statistic,
    variable,
    block,
    CAST(value AS DOUBLE) AS value
FROM "kenneth-french-data-library-25-portfolios-beme-inv-5x5-wout-div"
WHERE value IS NOT NULL
