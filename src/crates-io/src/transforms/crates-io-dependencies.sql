SELECT
    CAST(id AS BIGINT)                  AS id,
    CAST(version_id AS BIGINT)          AS version_id,
    CAST(crate_id AS BIGINT)            AS crate_id,
    req,
    CAST(COALESCE(kind, '0') AS INTEGER) AS kind,
    (optional = 't')                    AS optional,
    (default_features = 't')            AS default_features
FROM "crates-io-dependencies"
WHERE id IS NOT NULL AND version_id IS NOT NULL AND crate_id IS NOT NULL
