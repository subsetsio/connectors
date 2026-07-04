SELECT
    series_key,
    time_period,
    CAST(obs_value AS DOUBLE) AS value,
    obs_status,
    title,
    unit,
    CAST(unit_mult AS BIGINT) AS unit_mult
FROM "ecb-pfbr"
WHERE obs_value IS NOT NULL
  AND TRY_CAST(obs_value AS DOUBLE) IS NOT NULL
