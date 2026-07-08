SELECT
    CAST(dataset_id AS VARCHAR)              AS dataset_id,
    CAST(name AS VARCHAR)                    AS name,
    CAST(title AS VARCHAR)                   AS title,
    CAST(organization AS VARCHAR)            AS organization,
    CAST(subjects AS VARCHAR)                AS subjects,
    CAST(keywords AS VARCHAR)                AS keywords,
    CAST(license_id AS VARCHAR)              AS license_id,
    CAST(resource_formats AS VARCHAR)        AS resource_formats,
    CAST(num_resources AS INTEGER)           AS num_resources,
    CAST(notes AS VARCHAR)                   AS notes,
    TRY_CAST(metadata_created AS TIMESTAMP)  AS metadata_created,
    TRY_CAST(metadata_modified AS TIMESTAMP) AS metadata_modified,
    TRY_CAST(portal_release_date AS DATE)    AS portal_release_date
FROM "open-government-canada-datasets"
WHERE dataset_id IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY dataset_id ORDER BY metadata_modified DESC NULLS LAST
) = 1
