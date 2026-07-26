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
    "Free Application for Federal Student Aid (FAFSA) Submissions by High School Applications processed through April 9 of the first 15 months of each cycle" AS free_application_for_federal_student_aid_fafsa_submissions_by_high_school_applications_processed_through_april_9_of_the_first_15_months_of_each_cycle,
    "Unnamed: 1" AS unnamed_1,
    "Unnamed: 2" AS unnamed_2,
    "Unnamed: 3" AS unnamed_3,
    "Unnamed: 4" AS unnamed_4,
    "Unnamed: 5" AS unnamed_5,
    "Unnamed: 6" AS unnamed_6,
    "Unnamed: 7" AS unnamed_7,
    "Unnamed: 8" AS unnamed_8,
    "Unnamed: 9" AS unnamed_9,
    "Unnamed: 10" AS unnamed_10,
    "Free Application for Federal Student Aid (FAFSA) Estimated Completion Rates by Public School District Applications processed through April 9 of the first 15 months of each cycle" AS free_application_for_federal_student_aid_fafsa_estimated_completion_rates_by_public_school_district_applications_processed_through_april_9_of_the_first_15_months_of_each_cycle
FROM "u-s-department-of-education-fafsa-completion-by-high-school-and-public-school-district"
