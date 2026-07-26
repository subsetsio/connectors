-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Catalog-level dataset may contain mixed measures, geography levels, or reporting periods; inspect column definitions before aggregating.
SELECT
    "_subsets_record_type" AS subsets_record_type,
    "package_id",
    "package_title",
    "package_name",
    "metadata_modified",
    "resource_count",
    "skipped_resource_count"
FROM "u-s-department-of-education-edfacts-teacher-quality-2010-11-bfb3c"
