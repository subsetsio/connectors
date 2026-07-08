SELECT
    measure_id,
    TRY_CAST(date AS DATE) AS date,
    TRY_CAST(date_time AS TIMESTAMP) AS observed_at,
    TRY_CAST(value AS DOUBLE) AS value,
    quality
FROM "defra-hydrology-readings"
WHERE measure_id IS NOT NULL
  AND TRY_CAST(value AS DOUBLE) IS NOT NULL
