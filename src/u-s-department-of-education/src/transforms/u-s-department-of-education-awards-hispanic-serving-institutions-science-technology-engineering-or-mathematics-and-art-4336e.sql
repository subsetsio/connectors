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
    "Unnamed: 0" AS unnamed_0,
    "PR Number" AS pr_number,
    "Institution Name" AS institution_name,
    "State" AS state,
    "FY 2008 Awards" AS fy_2008_awards,
    "FY 2009 Estimated Amounts" AS fy_2009_estimated_amounts
FROM "u-s-department-of-education-awards-hispanic-serving-institutions-science-technology-engineering-or-mathematics-and-art-4336e"
