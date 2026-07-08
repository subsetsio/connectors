SELECT DISTINCT
    provider,
    timeseries_id,
    station_id,
    variable_code,
    variable_name,
    unit,
    aggregation,
    interpolation,
    CAST(period_begin AS TIMESTAMP) AS period_begin,
    CAST(period_end   AS TIMESTAMP) AS period_end
FROM "wmo-stations"
WHERE timeseries_id IS NOT NULL
