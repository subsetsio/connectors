-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows cover HIV/AIDS notifications and deaths by cause and sex; avoid adding sex-specific counts to totals if present.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "Case" AS case,
    "Type" AS type,
    CAST("Male" AS BIGINT) AS male,
    CAST("Female" AS BIGINT) AS female,
    "Underlying_Cause_of_Death" AS underlying_cause_of_death,
    "__row_number" AS row_number,
    "__package_id" AS package_id,
    "__package_name" AS package_name,
    "__package_title" AS package_title,
    CAST("__package_metadata_modified" AS TIMESTAMP) AS package_metadata_modified,
    "__resource_id" AS resource_id,
    "__resource_name" AS resource_name,
    "__resource_format" AS resource_format,
    CAST("__resource_last_modified" AS TIMESTAMP) AS resource_last_modified
FROM "statistics-mauritius-statistics-relating-notification-hiv-aids-cases-and-deaths-mauritius"
