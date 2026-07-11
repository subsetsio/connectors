SELECT
    CAST(id AS BIGINT) AS id,
    code,
    ref,
    name,
    organisation_type_name
FROM "itc-organisations"
WHERE id IS NOT NULL
