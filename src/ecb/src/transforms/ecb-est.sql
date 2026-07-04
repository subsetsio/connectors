SELECT
    series_key,
    time_period,
    CAST(obs_value AS DOUBLE) AS value,
    title,
    CAST(unit_mult AS BIGINT) AS unit_mult
FROM "ecb-est"
WHERE obs_value IS NOT NULL
  AND TRY_CAST(obs_value AS DOUBLE) IS NOT NULL
