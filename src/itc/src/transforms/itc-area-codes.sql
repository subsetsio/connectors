SELECT
    CAST(id AS BIGINT)          AS id,
    code,
    name,
    CAST(latitude AS DOUBLE)    AS latitude,
    CAST(longitude AS DOUBLE)   AS longitude,
    capital,
    kind,
    CAST(parent_id AS BIGINT)   AS parent_id,
    CAST(group_id AS BIGINT)    AS group_id,
    group_code,
    group_name,
    CAST(group_type AS INTEGER) AS group_type,
    row_type
FROM "itc-area-codes"
WHERE id IS NOT NULL
