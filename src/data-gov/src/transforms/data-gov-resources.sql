SELECT
    id,
    package_id,
    dataset_name,
    organization,
    name,
    description,
    format,
    mimetype,
    TRY_CAST(size AS BIGINT) AS size_bytes,
    TRY_CAST(created AS TIMESTAMP) AS created,
    TRY_CAST(last_modified AS TIMESTAMP) AS last_modified,
    state,
    resource_type,
    url_type,
    url
FROM (
    SELECT
        *,
        row_number() OVER (
            PARTITION BY id ORDER BY created DESC
        ) AS rn
    FROM "data-gov-resources"
)
WHERE rn = 1 AND id IS NOT NULL
