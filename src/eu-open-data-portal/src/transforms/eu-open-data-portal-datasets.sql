SELECT
    CAST(id AS VARCHAR)                  AS dataset_id,
    CAST(title AS VARCHAR)               AS title,
    CAST(description AS VARCHAR)         AS description,
    CAST(catalog AS VARCHAR)             AS catalog,
    CAST(country AS VARCHAR)             AS country,
    CAST(publisher AS VARCHAR)           AS publisher,
    CAST(categories AS VARCHAR)          AS categories,
    CAST(keywords AS VARCHAR)            AS keywords,
    TRY_CAST(modified AS DATE)           AS modified,
    TRY_CAST(issued AS DATE)             AS issued,
    CAST(landing_page AS VARCHAR)        AS landing_page,
    CAST(num_distributions AS INTEGER)   AS num_distributions,
    CAST(distribution_formats AS VARCHAR) AS distribution_formats,
    CAST(is_hvd AS BOOLEAN)              AS is_hvd
FROM "eu-open-data-portal-datasets"
WHERE id IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY id ORDER BY modified DESC NULLS LAST) = 1
