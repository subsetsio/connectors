SELECT
    series_key,
    freq,
    time_period,
    CAST(obs_value AS DOUBLE) AS value,
    title
FROM "ecb-inw"
WHERE obs_value IS NOT NULL
  AND TRY_CAST(obs_value AS DOUBLE) IS NOT NULL
