SELECT id, display_name,
       CAST(works_count AS BIGINT)    AS works_count,
       CAST(cited_by_count AS BIGINT) AS cited_by_count,
       TRY_CAST(updated_date AS TIMESTAMP) AS updated_at
FROM "openalex-keywords" WHERE id IS NOT NULL
