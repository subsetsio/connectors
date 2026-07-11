-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    CAST("__sheet__" AS BIGINT) AS sheet,
    "Sub-total" AS sub_total,
    "1406.1000000000001" AS 1406_1000000000001,
    "3800",
    "2.7" AS 2_7,
    "97.5" AS 97_5,
    "0.817" AS 0_817,
    "137074.9" AS 137074_9,
    "1550.8" AS 1550_8,
    "3877.1" AS 3877_1,
    "2.5" AS 2_5,
    "156.78" AS 156_78,
    "0.6343" AS 0_6343,
    "243140.1" AS 243140_1
FROM "gpih-kenya-1914-1927"
