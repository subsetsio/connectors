-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Reference-style source extract without a verified compact key; use the source columns as descriptive records rather than aggregating rows.
SELECT
    "resource_id",
    "resource_name",
    "group_id",
    "group_name",
    "group_title",
    "group_description",
    CAST("package_count" AS BIGINT) AS package_count,
    "package_id",
    "package_name",
    "package_title",
    "package_state",
    "organization",
    CAST("metadata_modified" AS TIMESTAMP) AS metadata_modified,
    "license_id"
FROM "public-health-scotland-ambulance-services"
