SELECT
    series_key,
    freq,
    time_period,
    CAST(obs_value AS DOUBLE) AS value,
    obs_status,
    title,
    CAST(unit_mult AS BIGINT) AS unit_mult
FROM "ecb-resh"
WHERE obs_value IS NOT NULL
  AND TRY_CAST(obs_value AS DOUBLE) IS NOT NULL
