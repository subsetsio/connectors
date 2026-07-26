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
    "row_number",
    "School Name" AS school_name,
    "City" AS city,
    "State" AS state,
    "District Name" AS district_name,
    "2010/11/Award Amount" AS 2010_11_award_amount,
    "Model Selected" AS model_selected,
    "Location" AS location
FROM "u-s-department-of-education-school-improvement-2010-grants-7ba90"
