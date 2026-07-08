SELECT
    CAST(version_id AS BIGINT)          AS version_id,
    CAST(date AS DATE)                  AS date,
    CAST(downloads AS BIGINT)           AS downloads
FROM "crates-io-version-downloads-daily"
WHERE version_id IS NOT NULL AND date IS NOT NULL
