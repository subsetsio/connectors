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
    "Extraction Date:" AS extraction_date,
    "7/30/2025" AS 7_30_2025,
    "Unnamed: 2" AS unnamed_2,
    "Unnamed: 3" AS unnamed_3,
    "-8 Data suppressed due to small cell size" AS 8_data_suppressed_due_to_small_cell_size,
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
    "Unnamed: 21" AS unnamed_21,
    "Unnamed: 22" AS unnamed_22,
    "Unnamed: 23" AS unnamed_23,
    "Unnamed: 24" AS unnamed_24,
    "Unnamed: 25" AS unnamed_25,
    "7/31/2024" AS 7_31_2024
FROM "u-s-department-of-education-idea-section-618-lea-part-b-educational-environments"
