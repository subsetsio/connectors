-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table combines GitHub-reviewed advisories with unreviewed CVE mirrors; use source_directory and github_reviewed when separating reviewed records from mirrored records.
SELECT
    "ghsa_id",
    "cve_id",
    "aliases",
    "summary",
    "severity",
    "cvss_v3_vector",
    "cvss_v4_vector",
    "cwe_ids",
    "github_reviewed",
    "published_at",
    "modified_at",
    "withdrawn_at",
    "github_reviewed_at",
    "nvd_published_at",
    "source_directory"
FROM "github-advisories"
