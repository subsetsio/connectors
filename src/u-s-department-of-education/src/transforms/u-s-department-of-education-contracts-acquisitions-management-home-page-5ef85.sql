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
    "Contract Number" AS contract_number,
    "Order/Call" AS order_call,
    "Contractor" AS contractor,
    "CO" AS co,
    "Contracting Office" AS contracting_office,
    "Award Date" AS award_date,
    "Current End Date" AS current_end_date,
    "Ultimate Completion Date" AS ultimate_completion_date,
    "Current Contract Value" AS current_contract_value,
    "Description" AS description
FROM "u-s-department-of-education-contracts-acquisitions-management-home-page-5ef85"
