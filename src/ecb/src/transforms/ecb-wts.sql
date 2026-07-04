SELECT
    series_key,
    CAST(time_period AS BIGINT) AS time_period,
    CAST(obs_value AS DOUBLE) AS value,
    obs_status,
    title
FROM "ecb-wts"
WHERE obs_value IS NOT NULL
  AND TRY_CAST(obs_value AS DOUBLE) IS NOT NULL
