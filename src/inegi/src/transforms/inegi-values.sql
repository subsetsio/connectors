SELECT
    indicator_id,
    topic_id,
    freq_id,
    unit_id,
    source_id,
    time_period,
    CAST(obs_value AS DOUBLE) AS value,
    obs_status,
    cober_geo AS coverage_geo,
    last_update
FROM "inegi-values"
WHERE obs_value IS NOT NULL
  AND TRY_CAST(obs_value AS DOUBLE) IS NOT NULL
