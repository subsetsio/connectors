SELECT id, display_name, ror, type, country_code, homepage_url,
       city, region, geo_country,
       CAST(latitude AS DOUBLE)  AS latitude,
       CAST(longitude AS DOUBLE) AS longitude,
       CAST(works_count AS BIGINT)    AS works_count,
       CAST(cited_by_count AS BIGINT) AS cited_by_count,
       CAST(h_index AS INTEGER)       AS h_index,
       CAST(i10_index AS INTEGER)     AS i10_index,
       CAST(mean_citedness AS DOUBLE) AS mean_citedness,
       TRY_CAST(created_date AS DATE)      AS created_date,
       TRY_CAST(updated_date AS TIMESTAMP) AS updated_at
FROM "openalex-institutions" WHERE id IS NOT NULL
