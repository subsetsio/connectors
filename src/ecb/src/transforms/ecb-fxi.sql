SELECT
    series_key,
    time_period,
    CAST(obs_value AS DOUBLE) AS value,
    title
FROM "ecb-fxi"
WHERE obs_value IS NOT NULL
  AND TRY_CAST(obs_value AS DOUBLE) IS NOT NULL
