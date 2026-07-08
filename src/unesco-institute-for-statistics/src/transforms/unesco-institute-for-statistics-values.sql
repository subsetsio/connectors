SELECT DISTINCT
    indicator_id,
    geo_unit,
    CAST(year AS INTEGER)  AS year,
    CAST(value AS DOUBLE)  AS value,
    magnitude,
    qualifier
FROM "unesco-institute-for-statistics-values"
WHERE indicator_id IS NOT NULL
  AND geo_unit IS NOT NULL
  AND year IS NOT NULL
  AND value IS NOT NULL
