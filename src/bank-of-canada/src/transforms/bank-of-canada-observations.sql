SELECT
    series_id,
    obs_index_key,
    obs_index,
    TRY_CAST(obs_date AS DATE) AS obs_date,
    value,
    TRY_CAST(value AS DOUBLE) AS value_number
FROM "bank-of-canada-observations"
WHERE series_id IS NOT NULL
  AND obs_index_key IS NOT NULL
  AND obs_index IS NOT NULL
