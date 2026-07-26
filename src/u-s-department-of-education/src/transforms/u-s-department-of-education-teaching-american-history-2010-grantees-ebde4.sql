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
    "District" AS district,
    "Project Title" AS project_title,
    "City" AS city,
    "State" AS state,
    "Amount" AS amount,
    "ZIP" AS zip,
    "projectdirector",
    "numteachers",
    "schooldistricts",
    "grades",
    "partners",
    "topics",
    "methods",
    "abstract",
    "Location" AS location
FROM "u-s-department-of-education-teaching-american-history-2010-grantees-ebde4"
