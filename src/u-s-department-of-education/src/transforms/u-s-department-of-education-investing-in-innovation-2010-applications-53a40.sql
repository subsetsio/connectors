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
    "Project Title" AS project_title,
    "City" AS city,
    "State" AS state,
    "Organization Zip" AS organization_zip,
    "Project Description" AS project_description,
    "Absolute Priority" AS absolute_priority,
    "Competitive Preference Priority" AS competitive_preference_priority,
    "Applicant Type" AS applicant_type,
    "Grant Type" AS grant_type,
    "Award Length" AS award_length,
    "Award Requested" AS award_requested,
    "Private Match Waiver" AS private_match_waiver,
    "Location" AS location
FROM "u-s-department-of-education-investing-in-innovation-2010-applications-53a40"
