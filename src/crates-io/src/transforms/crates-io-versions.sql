SELECT
    CAST(id AS BIGINT)                  AS id,
    CAST(crate_id AS BIGINT)            AS crate_id,
    num                                 AS version,
    CAST(COALESCE(downloads, '0') AS BIGINT) AS downloads,
    CAST(crate_size AS BIGINT)          AS crate_size,
    license,
    CAST(created_at AS TIMESTAMP)       AS created_at,
    (yanked = 't')                      AS yanked
FROM "crates-io-versions"
WHERE id IS NOT NULL AND crate_id IS NOT NULL AND num IS NOT NULL
