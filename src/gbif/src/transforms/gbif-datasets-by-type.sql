SELECT facet_value         AS dataset_type,
       CAST(n AS BIGINT)    AS dataset_count
FROM "gbif-datasets-by-type"
WHERE facet_value IS NOT NULL
ORDER BY dataset_count DESC
