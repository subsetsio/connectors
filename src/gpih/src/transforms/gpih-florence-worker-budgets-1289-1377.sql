-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "Oil" AS "oil",
    "1",
    "kg",
    "1_2",
    "6",
    "1.5" AS "1_5",
    "2",
    "7",
    "2.5833333333333335" AS "2_5833333333333335",
    "3",
    "2_2",
    "3.1666666666666665" AS "3_1666666666666665",
    "3_2",
    "8",
    "3.6666666666666665" AS "3_6666666666666665",
    "3_3",
    "2_3",
    "3.1666666666666665_2" AS "3_1666666666666665_2",
    "5",
    "4",
    "5.333333333333333" AS "5_333333333333333"
FROM "gpih-florence-worker-budgets-1289-1377"
