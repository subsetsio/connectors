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
    "DEPARTMENT OF EDUCATION" AS department_of_education,
    "No data" AS no_data,
    "No data.1" AS no_data_1,
    "No data.2" AS no_data_2,
    "No data.3" AS no_data_3,
    "No data.4" AS no_data_4,
    "No Data_1" AS no_data_1_2,
    "No Data.1_1" AS no_data_1_1,
    "No Data.2_1" AS no_data_2_1,
    "No Data.3_1" AS no_data_3_1,
    "No Data.4_1" AS no_data_4_1
FROM "u-s-department-of-education-fiscal-year-2019-fy-2021-presidents-budget-state-tables-for-the-u-s-department-of-educatio"
