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
    "Free Application for Federal Student Aid (FAFSA) By Various Demographic Characteristics 2009/10 Application Cycle" AS free_application_for_federal_student_aid_fafsa_by_various_demographic_characteristics_2009_10_application_cycle,
    "Unnamed: 1" AS unnamed_1,
    "Unnamed: 2" AS unnamed_2,
    "Unnamed: 3" AS unnamed_3,
    "Unnamed: 4" AS unnamed_4,
    "Unnamed: 5" AS unnamed_5,
    "Unnamed: 6" AS unnamed_6,
    "Unnamed: 7" AS unnamed_7,
    "Unnamed: 8" AS unnamed_8,
    "Application Data by School" AS application_data_by_school,
    "Unnamed: 9" AS unnamed_9,
    "Unnamed: 10" AS unnamed_10
FROM "u-s-department-of-education-free-application-for-federal-student-aid-2009-10-49629"
