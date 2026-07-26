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
    "Grantee Institution" AS grantee_institution,
    "State" AS state,
    "FY 2011 Award Amount" AS fy_2011_award_amount,
    "PR Award No." AS pr_award_no,
    "Institution" AS institution,
    "Recommended Grant Amount" AS recommended_grant_amount
FROM "u-s-department-of-education-awards-predominantly-black-institutions-program-formula-grants-ff8e8"
