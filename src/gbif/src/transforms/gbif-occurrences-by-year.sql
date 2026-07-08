SELECT TRY_CAST(facet_value AS INTEGER) AS year,
       CAST(n AS BIGINT)                AS occurrence_count
FROM "gbif-occurrences-by-year"
WHERE TRY_CAST(facet_value AS INTEGER) IS NOT NULL
  AND TRY_CAST(facet_value AS INTEGER) > 0
ORDER BY year
