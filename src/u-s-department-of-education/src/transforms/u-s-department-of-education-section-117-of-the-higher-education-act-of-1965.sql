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
    "Foreign Schools Gift and Contracts Report with Date Range 01/01/2014 to 12/31/2019 Grouped by: OPEID, State, Foreign Gift Received Date Data Source: Postsecondary Education Participation System 3/30/2020" AS foreign_schools_gift_and_contracts_report_with_date_range_01_01_2014_to_12_31_2019_grouped_by_opeid_state_foreign_gift_received_date_data_source_postsecondary_education_participation_system_3_30_2020,
    "Unnamed: 1" AS unnamed_1,
    "Unnamed: 2" AS unnamed_2,
    "Unnamed: 3" AS unnamed_3,
    "Unnamed: 4" AS unnamed_4,
    "Unnamed: 5" AS unnamed_5,
    "Unnamed: 6" AS unnamed_6,
    "Unnamed: 7" AS unnamed_7,
    "Unnamed: 8" AS unnamed_8,
    "Unnamed: 9" AS unnamed_9
FROM "u-s-department-of-education-section-117-of-the-higher-education-act-of-1965"
