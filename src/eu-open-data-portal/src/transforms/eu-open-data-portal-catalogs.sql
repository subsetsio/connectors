SELECT
    CAST(id AS VARCHAR)            AS catalog_id,
    CAST(title AS VARCHAR)         AS title,
    CAST(publisher AS VARCHAR)     AS publisher,
    CAST(country AS VARCHAR)       AS country,
    CAST(source_type AS VARCHAR)   AS source_type,
    TRY_CAST(issued AS DATE)       AS issued,
    TRY_CAST(modified AS DATE)     AS modified,
    CAST(dataset_count AS BIGINT)  AS dataset_count,
    CAST(description AS VARCHAR)   AS description
FROM "eu-open-data-portal-catalogs"
WHERE id IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY id ORDER BY modified DESC NULLS LAST) = 1
