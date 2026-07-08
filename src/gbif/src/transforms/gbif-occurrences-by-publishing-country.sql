SELECT facet_value         AS publishing_country,
       CAST(n AS BIGINT)    AS occurrence_count
FROM "gbif-occurrences-by-publishing-country"
WHERE facet_value IS NOT NULL
ORDER BY occurrence_count DESC
