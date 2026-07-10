SELECT
    id,
    title,
    description,
    source_type,
    country_id,
    publisher_name,
    publisher_resource,
    issued,
    modified,
    dataset_count
FROM "eu-open-data-portal-catalogs"
WHERE id IS NOT NULL
