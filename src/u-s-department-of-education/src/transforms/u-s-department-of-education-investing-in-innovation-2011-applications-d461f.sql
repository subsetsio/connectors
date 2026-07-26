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
    "Absolute Priority" AS absolute_priority,
    "PR Award No" AS pr_award_no,
    "Length of Requested Grant Award" AS length_of_requested_grant_award,
    "Type Of Grant Requested" AS type_of_grant_requested,
    "Project Description" AS project_description,
    "Federal Funding Requested" AS federal_funding_requested,
    "CPP10" AS cpp10,
    "CPP9" AS cpp9,
    "CPP8" AS cpp8,
    "CPP7" AS cpp7,
    "CPP6" AS cpp6,
    "HighestRated" AS highestrated,
    "Location" AS location
FROM "u-s-department-of-education-investing-in-innovation-2011-applications-d461f"
