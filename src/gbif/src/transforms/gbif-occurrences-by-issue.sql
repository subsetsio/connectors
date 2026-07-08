SELECT facet_value         AS issue,
       CAST(n AS BIGINT)    AS occurrence_count
FROM "gbif-occurrences-by-issue"
WHERE facet_value IS NOT NULL
ORDER BY occurrence_count DESC
