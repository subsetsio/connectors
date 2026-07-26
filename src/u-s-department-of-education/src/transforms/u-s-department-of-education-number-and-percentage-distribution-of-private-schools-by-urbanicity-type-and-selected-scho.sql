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
    "Table 4. Number and percentage distribution of private schools, by urbanicity type and selected school characteristics: United States, 2017–18" AS table_4_number_and_percentage_distribution_of_private_schools_by_urbanicity_type_and_selected_school_characteristics_united_states_2017_18,
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
    "Unnamed: 12" AS unnamed_12,
    "Unnamed: 13" AS unnamed_13,
    "Unnamed: 14" AS unnamed_14,
    "Unnamed: 15" AS unnamed_15,
    "Unnamed: 16" AS unnamed_16,
    "Unnamed: 17" AS unnamed_17,
    "Unnamed: 18" AS unnamed_18,
    "Unnamed: 19" AS unnamed_19,
    "Unnamed: 20" AS unnamed_20,
    "Table C-4. Standard errors for the number and percentage distribution of private schools, by urbanicity type and selected school characteristics: United States, 2017–18" AS table_c_4_standard_errors_for_the_number_and_percentage_distribution_of_private_schools_by_urbanicity_type_and_selected_school_characteristics_united_states_2017_18
FROM "u-s-department-of-education-number-and-percentage-distribution-of-private-schools-by-urbanicity-type-and-selected-scho"
