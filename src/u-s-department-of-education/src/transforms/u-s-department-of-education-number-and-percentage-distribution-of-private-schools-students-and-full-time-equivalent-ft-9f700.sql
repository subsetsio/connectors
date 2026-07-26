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
    "Table 1. Number and percentage distribution of private schools, students, and full-time equivalent (FTE) teachers, by selected school characteristics: United States, 2017–18" AS table_1_number_and_percentage_distribution_of_private_schools_students_and_full_time_equivalent_fte_teachers_by_selected_school_characteristics_united_states_2017_18,
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
    "Unnamed: 11" AS unnamed_11,
    "Table C-1. Standard errors for table 1: number and percentage distribution of private schools, students," AS table_c_1_standard_errors_for_table_1_number_and_percentage_distribution_of_private_schools_students,
    "Unnamed: 12" AS unnamed_12,
    "Unnamed: 13" AS unnamed_13
FROM "u-s-department-of-education-number-and-percentage-distribution-of-private-schools-students-and-full-time-equivalent-ft-9f700"
