SELECT
    CAST(id AS BIGINT) AS id,
    CAST(code AS VARCHAR) AS code,
    CAST(ref AS VARCHAR) AS ref,
    CAST(name AS VARCHAR) AS name,
    CAST(organisation_type_name AS VARCHAR) AS organisation_type_name
FROM "itc-organisations"
WHERE id IS NOT NULL
