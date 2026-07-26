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
    "DISTRIBUTION OF FEDERAL TEACH GRANT RECIPIENTS" AS distribution_of_federal_teach_grant_recipients,
    "Unnamed: 1" AS unnamed_1,
    "Unnamed: 2" AS unnamed_2,
    "Unnamed: 3" AS unnamed_3,
    "Unnamed: 4" AS unnamed_4,
    "Unnamed: 5" AS unnamed_5,
    "Unnamed: 6" AS unnamed_6,
    "Distribution of TEACH Grant Program Recipients and Awards" AS distribution_of_teach_grant_program_recipients_and_awards,
    "Distribution of the TEACH Grant Program" AS distribution_of_the_teach_grant_program,
    "Unnamed: 7" AS unnamed_7
FROM "u-s-department-of-education-distribution-of-federal-teach-grant-program-funds-by-institution-and-award-year-1a983"
