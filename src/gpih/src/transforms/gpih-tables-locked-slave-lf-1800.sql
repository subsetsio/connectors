-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "CONNECTICUT" AS connecticut,
    "578.7" AS 578_7,
    "410.646" AS 410_646,
    "168.05400000000003" AS 168_05400000000003,
    "77.83553684210527" AS 77_83553684210527,
    "90.21846315789476" AS 90_21846315789476,
    "0",
    "Connecticut_1" AS connecticut_1
FROM "gpih-tables-locked-slave-lf-1800"
