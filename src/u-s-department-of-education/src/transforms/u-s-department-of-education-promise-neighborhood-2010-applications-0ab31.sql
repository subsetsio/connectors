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
    "Applicant" AS applicant,
    "City" AS city,
    "State" AS state,
    "Absolute Priority" AS absolute_priority,
    "Applicant Type" AS applicant_type,
    "Location" AS location
FROM "u-s-department-of-education-promise-neighborhood-2010-applications-0ab31"
