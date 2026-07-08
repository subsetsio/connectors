SELECT
    indicator_id,
    area,
    CAST(year AS INTEGER)       AS year,
    TRY_CAST(value AS DOUBLE)   AS value,
    unit,
    disaggregation
FROM "nbs-tanzania-values"
WHERE indicator_id IS NOT NULL
  AND TRY_CAST(value AS DOUBLE) IS NOT NULL
