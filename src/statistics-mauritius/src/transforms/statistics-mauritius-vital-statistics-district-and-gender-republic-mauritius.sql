-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix district and gender breakdowns; filter to one geography and gender level before aggregating vital events.
SELECT
    CAST("year" AS BIGINT) AS year,
    "island",
    "district",
    "category",
    CAST("male" AS BIGINT) AS male,
    CAST("female" AS BIGINT) AS female,
    "__row_number" AS row_number,
    "__package_id" AS package_id,
    "__package_name" AS package_name,
    "__package_title" AS package_title,
    CAST("__package_metadata_modified" AS TIMESTAMP) AS package_metadata_modified,
    "__resource_id" AS resource_id,
    "__resource_name" AS resource_name,
    "__resource_format" AS resource_format,
    CAST("__resource_last_modified" AS TIMESTAMP) AS resource_last_modified
FROM "statistics-mauritius-vital-statistics-district-and-gender-republic-mauritius"
