WITH ranked AS (
    SELECT
        package_id,
        version,
        commit_timestamp,
        is_delete,
        row_number() OVER (
            PARTITION BY lower(package_id), version
            ORDER BY commit_timestamp DESC
        ) AS rn
    FROM "nuget-package-versions"
)
SELECT
    package_id,
    version,
    CAST(commit_timestamp AS TIMESTAMP) AS published,
    (version LIKE '%-%') AS is_prerelease
FROM ranked
WHERE rn = 1 AND is_delete = FALSE
