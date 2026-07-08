SELECT
    CAST(period AS DATE)  AS date,
    series_code,
    variable,
    region,
    measure,
    weighting,
    label,
    CAST(value AS DOUBLE) AS value
FROM "cpb-world-trade-monitor-values"
WHERE value IS NOT NULL
