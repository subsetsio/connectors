SELECT id, display_name, alternate_titles, country_codes,
       CAST(hierarchy_level AS INTEGER) AS hierarchy_level,
       parent_publisher,
       CAST(works_count AS BIGINT)      AS works_count,
       CAST(cited_by_count AS BIGINT)   AS cited_by_count,
       CAST(h_index AS INTEGER)         AS h_index,
       CAST(i10_index AS INTEGER)       AS i10_index,
       CAST(mean_citedness AS DOUBLE)   AS mean_citedness,
       ror, wikidata,
       TRY_CAST(created_date AS DATE)        AS created_date,
       TRY_CAST(updated_date AS TIMESTAMP)   AS updated_at
FROM "openalex-publishers" WHERE id IS NOT NULL
