SELECT
    CAST(id AS BIGINT)         AS id,
    name,
    short_name,
    slug,
    description,
    CAST(parent_id AS BIGINT)  AS parent_id,
    agency_url,
    child_count
FROM "federal-register-agencies"
WHERE id IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY id ORDER BY slug) = 1
