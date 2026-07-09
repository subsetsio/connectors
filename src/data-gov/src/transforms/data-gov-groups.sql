SELECT
    id,
    name,
    title,
    display_name,
    description,
    TRY_CAST(package_count AS INTEGER) AS package_count,
    type,
    state,
    TRY_CAST(created AS TIMESTAMP) AS created,
    TRY_CAST(num_followers AS INTEGER) AS num_followers,
    is_organization,
    approval_status
FROM "data-gov-groups"
WHERE id IS NOT NULL
