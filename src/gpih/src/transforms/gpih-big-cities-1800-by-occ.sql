-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "artisans",
    "69",
    "611",
    "0.18543247344461306" AS "0_18543247344461306",
    "32",
    "0.0886426592797784" AS "0_0886426592797784",
    "643",
    "643_2",
    "643_3",
    "0.1759233926128591" AS "0_1759233926128591",
    "c10",
    "c11",
    "artisans_2",
    "69_2",
    "643_4",
    "0.1759233926128591_2" AS "0_1759233926128591_2",
    "32_2",
    "0.0886426592797784_2" AS "0_0886426592797784_2",
    "Boston" AS "boston",
    "White collar" AS "white_collar",
    "0.4194254445964432" AS "0_4194254445964432",
    "c3",
    "0.363" AS "0_363"
FROM "gpih-big-cities-1800-by-occ"
