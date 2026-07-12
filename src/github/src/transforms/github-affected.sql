-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are package-range records exploded from advisories; an advisory can affect multiple packages and ranges, so do not count rows as distinct advisories without grouping by ghsa_id.
-- caution: The raw source can repeat identical package-range rows for a small number of records, so this table is intentionally keyless.
SELECT
    "ghsa_id",
    "ecosystem",
    "package_name",
    "vulnerable_version_range",
    "first_patched_version",
    "source_directory"
FROM "github-affected"
