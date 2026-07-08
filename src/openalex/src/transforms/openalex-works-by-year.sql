SELECT CAST(publication_year AS INTEGER) AS publication_year,
       CAST(works_count AS BIGINT)       AS works_count
FROM "openalex-works-by-year"
WHERE publication_year IS NOT NULL
  AND CAST(publication_year AS INTEGER) BETWEEN 1500 AND 2100
ORDER BY publication_year
