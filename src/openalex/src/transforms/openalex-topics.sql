SELECT id, display_name, description,
       domain_id, domain_name, field_id, field_name,
       subfield_id, subfield_name, keywords,
       CAST(works_count AS BIGINT)    AS works_count,
       CAST(cited_by_count AS BIGINT) AS cited_by_count,
       TRY_CAST(updated_date AS TIMESTAMP) AS updated_at
FROM "openalex-topics" WHERE id IS NOT NULL
