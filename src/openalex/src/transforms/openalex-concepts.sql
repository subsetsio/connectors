SELECT id, display_name, description,
       CAST(level AS INTEGER) AS level,
       wikidata, ancestors, related_concepts,
       CAST(works_count AS BIGINT)    AS works_count,
       CAST(cited_by_count AS BIGINT) AS cited_by_count,
       CAST(h_index AS INTEGER)       AS h_index,
       CAST(i10_index AS INTEGER)     AS i10_index,
       CAST(mean_citedness AS DOUBLE) AS mean_citedness,
       TRY_CAST(updated_date AS TIMESTAMP) AS updated_at
FROM "openalex-concepts" WHERE id IS NOT NULL
