SELECT
    package,
    version,
    CAST(published_at AS TIMESTAMP)         AS published_at,
    deprecated,
    deprecation_message,
    CAST(dependencies_count AS INTEGER)     AS dependencies_count,
    CAST(dev_dependencies_count AS INTEGER) AS dev_dependencies_count,
    CAST(unpacked_size_bytes AS BIGINT)     AS unpacked_size_bytes
FROM "npm-package-versions"
WHERE package IS NOT NULL AND version IS NOT NULL
