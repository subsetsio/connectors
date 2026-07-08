SELECT
    CAST(org_id AS VARCHAR)        AS org_id,
    CAST(name AS VARCHAR)          AS name,
    CAST(title AS VARCHAR)         AS title,
    CAST(package_count AS INTEGER) AS package_count,
    CAST(state AS VARCHAR)         AS state,
    CAST(type AS VARCHAR)          AS type,
    TRY_CAST(created AS TIMESTAMP) AS created
FROM "open-government-canada-organizations"
WHERE org_id IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY org_id ORDER BY package_count DESC NULLS LAST) = 1
