SELECT
    CAST(id AS BIGINT)                  AS id,
    name,
    description,
    CAST(COALESCE(downloads, '0') AS BIGINT) AS downloads,
    CAST(created_at AS TIMESTAMP)       AS created_at,
    CAST(updated_at AS TIMESTAMP)       AS updated_at,
    homepage,
    documentation,
    repository
FROM "crates-io-crates"
WHERE id IS NOT NULL AND name IS NOT NULL
