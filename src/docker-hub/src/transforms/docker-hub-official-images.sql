SELECT
    namespace,
    repo,
    description,
    repository_type,
    CAST(status AS INTEGER)               AS status,
    status_description,
    CAST(date_registered AS TIMESTAMP)    AS date_registered,
    CAST(last_updated AS TIMESTAMP)       AS last_updated,
    CAST(storage_size AS BIGINT)          AS storage_size_bytes,
    NULLIF(categories, '')                AS categories
FROM "docker-hub-official-images"
WHERE repo IS NOT NULL
