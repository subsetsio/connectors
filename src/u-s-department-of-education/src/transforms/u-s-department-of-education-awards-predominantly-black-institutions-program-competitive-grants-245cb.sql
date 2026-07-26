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
    "Predominatly Black Institutions - Competitive Grants - FY 2011 Awards" AS predominatly_black_institutions_competitive_grants_fy_2011_awards,
    "State" AS state,
    "FY 2011 Award Amount" AS fy_2011_award_amount,
    "Institution Name - New Awards" AS institution_name_new_awards,
    "FY 2009 Awards" AS fy_2009_awards,
    "Grantee Name" AS grantee_name,
    "FY 2008 Awards" AS fy_2008_awards
FROM "u-s-department-of-education-awards-predominantly-black-institutions-program-competitive-grants-245cb"
