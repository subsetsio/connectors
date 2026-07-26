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
    "Unnamed: 0" AS unnamed_0,
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
    "2007-01-24 00:00:00" AS 2007_01_24_00_00_00,
    "(in thousands of dollars)" AS in_thousands_of_dollars,
    "2007",
    "2007.1" AS 2007_1,
    "2008",
    "2008 President's Request" AS 2008_president_s_request
FROM "u-s-department-of-education-fy-2008-budget-summary-table-of-contents"
