-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include island-level and Republic of Mauritius values; filter geography before aggregating infant deaths or rates.
SELECT
    CAST("year" AS BIGINT) AS year,
    "country",
    CAST("infant_death" AS BIGINT) AS infant_death,
    CAST("infant_mortality_rate" AS DOUBLE) AS infant_mortality_rate,
    "__row_number" AS row_number,
    "__package_id" AS package_id,
    "__package_name" AS package_name,
    "__package_title" AS package_title,
    CAST("__package_metadata_modified" AS TIMESTAMP) AS package_metadata_modified,
    "__resource_id" AS resource_id,
    "__resource_name" AS resource_name,
    "__resource_format" AS resource_format,
    CAST("__resource_last_modified" AS TIMESTAMP) AS resource_last_modified
FROM "statistics-mauritius-infant-mortality-statistics-republic-mauritius"
