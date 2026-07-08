SELECT DISTINCT
    series_id,
    TRY_CAST(obs_date AS DATE)  AS date,
    TRY_CAST(value AS DOUBLE) AS value
FROM "bank-of-canada-observations"
WHERE series_id IS NOT NULL
  AND obs_date IS NOT NULL
  AND TRY_CAST(obs_date AS DATE) IS NOT NULL
  AND TRY_CAST(value AS DOUBLE) IS NOT NULL
