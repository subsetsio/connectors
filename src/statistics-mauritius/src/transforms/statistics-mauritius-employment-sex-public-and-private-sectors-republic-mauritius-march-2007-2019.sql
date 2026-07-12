-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows describe large establishments surveyed in March and mix public ministry and private-sector categories; compare only like sectors.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "Sex" AS sex,
    CAST("Government_Ministries/Departments" AS BIGINT) AS government_ministries_departments,
    CAST("Extra_Budgetary_Unit" AS BIGINT) AS extra_budgetary_unit,
    CAST("Regional_Government" AS BIGINT) AS regional_government,
    CAST("Local_Government" AS BIGINT) AS local_government,
    CAST("Public_Enterprises" AS BIGINT) AS public_enterprises,
    CAST("Privat_Sector" AS BIGINT) AS privat_sector,
    "__row_number" AS row_number,
    "__package_id" AS package_id,
    "__package_name" AS package_name,
    "__package_title" AS package_title,
    CAST("__package_metadata_modified" AS TIMESTAMP) AS package_metadata_modified,
    "__resource_id" AS resource_id,
    "__resource_name" AS resource_name,
    "__resource_format" AS resource_format,
    CAST("__resource_last_modified" AS TIMESTAMP) AS resource_last_modified
FROM "statistics-mauritius-employment-sex-public-and-private-sectors-republic-mauritius-march-2007-2019"
