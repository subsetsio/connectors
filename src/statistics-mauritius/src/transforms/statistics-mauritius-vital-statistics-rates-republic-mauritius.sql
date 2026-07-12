-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows contain vital-statistics rates rather than event counts; rates should not be summed across years or categories.
SELECT
    CAST("Year" AS BIGINT) AS year,
    CAST("Crude_Birth_Rate" AS DOUBLE) AS crude_birth_rate,
    CAST("Crude_Death_Rate" AS DOUBLE) AS crude_death_rate,
    CAST("Infant_Mortality_Rate" AS DOUBLE) AS infant_mortality_rate,
    CAST("Still_Birth_Rate" AS DOUBLE) AS still_birth_rate,
    CAST("Marriage_Rate" AS DOUBLE) AS marriage_rate,
    CAST("Divorce_Rate" AS DOUBLE) AS divorce_rate,
    "__row_number" AS row_number,
    "__package_id" AS package_id,
    "__package_name" AS package_name,
    "__package_title" AS package_title,
    CAST("__package_metadata_modified" AS TIMESTAMP) AS package_metadata_modified,
    "__resource_id" AS resource_id,
    "__resource_name" AS resource_name,
    "__resource_format" AS resource_format,
    CAST("__resource_last_modified" AS TIMESTAMP) AS resource_last_modified
FROM "statistics-mauritius-vital-statistics-rates-republic-mauritius"
