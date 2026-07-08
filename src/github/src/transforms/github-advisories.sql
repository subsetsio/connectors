SELECT
    ghsa_id,
    cve_id,
    aliases,
    summary,
    severity,
    cvss_v3_vector,
    cvss_v4_vector,
    cwe_ids,
    github_reviewed,
    try_cast(published_at AS TIMESTAMP)        AS published_at,
    try_cast(modified_at AS TIMESTAMP)         AS modified_at,
    try_cast(withdrawn_at AS TIMESTAMP)        AS withdrawn_at,
    try_cast(github_reviewed_at AS TIMESTAMP)  AS github_reviewed_at,
    try_cast(nvd_published_at AS TIMESTAMP)    AS nvd_published_at,
    source_directory
FROM "github-advisories"
WHERE ghsa_id IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY ghsa_id
    ORDER BY try_cast(modified_at AS TIMESTAMP) DESC NULLS LAST
) = 1
