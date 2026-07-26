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
    "PR NUMBER" AS pr_number,
    "STATE" AS state,
    "INSTITUTION" AS institution,
    "AWARD AMOUNT" AS award_amount,
    "Unnamed: 0" AS unnamed_0,
    "PR Number_1" AS pr_number_1,
    "Institution Name" AS institution_name,
    "State_1" AS state_1,
    "FY 2008 Awards" AS fy_2008_awards,
    "Unnamed: 5" AS unnamed_5,
    "State Totals" AS state_totals
FROM "u-s-department-of-education-awards-historically-black-colleges-and-universities-program-ccraa-c09ec"
