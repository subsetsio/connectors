-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "Top 1%:" AS "top_1",
    "14.531370959009" AS "14_531370959009",
    "20.9" AS "20_9",
    "18.4658443355017" AS "18_4658443355017",
    "19",
    "c5",
    "c6"
FROM "gpih-net-worth-summary-1774"
