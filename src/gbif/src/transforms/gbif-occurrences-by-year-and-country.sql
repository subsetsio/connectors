SELECT facet_value                AS country,
       TRY_CAST(year AS INTEGER)  AS year,
       CAST(n AS BIGINT)          AS occurrence_count
FROM "gbif-occurrences-by-year-and-country"
WHERE facet_value IS NOT NULL
  AND TRY_CAST(year AS INTEGER) IS NOT NULL
  AND TRY_CAST(year AS INTEGER) > 0
ORDER BY country, year
