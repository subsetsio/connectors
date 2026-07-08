SELECT
    package_id,
    latest_version,
    total_downloads,
    verified,
    version_count,
    authors,
    tags
FROM "nuget-packages"
WHERE package_id IS NOT NULL
