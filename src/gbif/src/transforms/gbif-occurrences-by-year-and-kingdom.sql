SELECT TRY_CAST(facet_value AS INTEGER) AS kingdom_key,
       TRY_CAST(year AS INTEGER)        AS year,
       CAST(n AS BIGINT)                AS occurrence_count
FROM "gbif-occurrences-by-year-and-kingdom"
WHERE TRY_CAST(facet_value AS INTEGER) IS NOT NULL
  AND TRY_CAST(year AS INTEGER) IS NOT NULL
  AND TRY_CAST(year AS INTEGER) > 0
ORDER BY kingdom_key, year
