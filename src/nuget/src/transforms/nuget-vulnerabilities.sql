SELECT
    package_id,
    advisory_url,
    severity,
    versions,
    page_name,
    CAST(page_updated AS TIMESTAMP) AS updated_at
FROM "nuget-vulnerabilities"
WHERE package_id IS NOT NULL
  AND advisory_url IS NOT NULL
  AND versions IS NOT NULL
