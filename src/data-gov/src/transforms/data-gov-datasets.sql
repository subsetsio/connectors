SELECT
    id,
    name,
    title,
    notes AS description,
    organization,
    owner_org,
    license_id,
    license_title,
    TRY_CAST(metadata_created AS TIMESTAMP) AS metadata_created,
    TRY_CAST(metadata_modified AS TIMESTAMP) AS metadata_modified,
    TRY_CAST(num_resources AS INTEGER) AS num_resources,
    TRY_CAST(num_tags AS INTEGER) AS num_tags,
    type,
    state,
    maintainer,
    author,
    version,
    url,
    tags,
    groups
FROM (
    SELECT
        *,
        row_number() OVER (
            PARTITION BY id ORDER BY metadata_modified DESC
        ) AS rn
    FROM "data-gov-datasets"
)
WHERE rn = 1 AND id IS NOT NULL
