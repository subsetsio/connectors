SELECT
    series_code,
    label,
    sheet,
    variable,
    region,
    measure,
    weighting,
    CAST(weight_2021 AS DOUBLE) AS weight_2021
FROM "cpb-world-trade-monitor-series"
