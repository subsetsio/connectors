-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS "sheet",
    "Beans" AS "beans",
    "5 kg" AS "5_kg",
    "3.27" AS "3_27",
    "2.7" AS "2_7",
    "46",
    "3"
FROM "gpih-sichuan-1905-bundle"
