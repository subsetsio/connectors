SELECT
    provider,
    timeseries_id,
    station_id,
    variable_code,
    variable_name,
    unit,
    CAST(observed_at AS TIMESTAMP) AS observed_at,
    CAST(value AS DOUBLE)          AS value
FROM (
    SELECT *, row_number() OVER (
        PARTITION BY provider, station_id, variable_code, observed_at
        ORDER BY value
    ) AS _rn
    FROM "wmo-values"
    WHERE observed_at IS NOT NULL
      AND value IS NOT NULL
)
WHERE _rn = 1
