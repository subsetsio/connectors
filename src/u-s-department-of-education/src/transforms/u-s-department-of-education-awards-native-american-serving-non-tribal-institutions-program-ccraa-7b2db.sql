-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Catalog-level dataset may contain mixed measures, geography levels, or reporting periods; inspect column definitions before aggregating.
SELECT
    "package_id",
    "package_title",
    "resource_id",
    "resource_name",
    "resource_format",
    "resource_position",
    "sheet_name",
    "row_number",
    "PR Number" AS pr_number,
    "NASNTI Grantee" AS nasnti_grantee,
    "State" AS state,
    "FY 2008 Awards" AS fy_2008_awards,
    "FY 2009 Estimated Awards" AS fy_2009_estimated_awards,
    "Total Estimated" AS total_estimated
FROM "u-s-department-of-education-awards-native-american-serving-non-tribal-institutions-program-ccraa-7b2db"
