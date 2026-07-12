-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows cover offence classifications for both Mauritius and Rodrigues; filter geography before comparing or aggregating counts.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "Island" AS island,
    "Offences" AS offences,
    "Offences_Type" AS offences_type,
    "Cat_Offences" AS cat_offences,
    "Sub_Cat_Offences" AS sub_cat_offences,
    "Description" AS description,
    "Number" AS number,
    "__row_number" AS row_number,
    "__package_id" AS package_id,
    "__package_name" AS package_name,
    "__package_title" AS package_title,
    CAST("__package_metadata_modified" AS TIMESTAMP) AS package_metadata_modified,
    "__resource_id" AS resource_id,
    "__resource_name" AS resource_name,
    "__resource_format" AS resource_format,
    CAST("__resource_last_modified" AS TIMESTAMP) AS resource_last_modified
FROM "statistics-mauritius-convicted-offences-according-un-classification-crime-statistical-purposes-mauritius-and"
