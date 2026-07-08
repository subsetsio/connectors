SELECT dimension,
       dimension_key,
       dimension_label,
       CAST(publication_year AS INTEGER) AS publication_year,
       CAST(works_count AS BIGINT)       AS works_count
FROM "openalex-works-by-dimension-year"
WHERE publication_year IS NOT NULL
  AND CAST(publication_year AS INTEGER) BETWEEN 1500 AND 2100
