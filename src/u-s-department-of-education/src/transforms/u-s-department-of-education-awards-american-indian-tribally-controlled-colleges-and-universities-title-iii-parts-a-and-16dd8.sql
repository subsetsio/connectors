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
    "TCCU Part A Grantee" AS tccu_part_a_grantee,
    "State" AS state,
    "FY 2013 Award Amount" AS fy_2013_award_amount,
    "FY 2011 Award Amount" AS fy_2011_award_amount
FROM "u-s-department-of-education-awards-american-indian-tribally-controlled-colleges-and-universities-title-iii-parts-a-and-16dd8"
