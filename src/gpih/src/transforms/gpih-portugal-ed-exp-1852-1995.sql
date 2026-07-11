-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "1853",
    "13",
    "0.5" AS 0_5,
    "296",
    "67.4" AS 67_4,
    "0.16891891891891891" AS 0_16891891891891891,
    "1946",
    "377.9" AS 377_9,
    "43",
    "420.9" AS 420_9,
    "10.216203373722974" AS 10_216203373722974,
    "11"
FROM "gpih-portugal-ed-exp-1852-1995"
