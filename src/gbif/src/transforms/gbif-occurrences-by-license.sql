SELECT facet_value         AS license,
       CAST(n AS BIGINT)    AS occurrence_count
FROM "gbif-occurrences-by-license"
WHERE facet_value IS NOT NULL
ORDER BY occurrence_count DESC
