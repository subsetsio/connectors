-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS sheet,
    "Meat" AS meat,
    "2 kg" AS 2_kg,
    "4.9" AS 4_9,
    "2.1" AS 2_1,
    "14",
    "1"
FROM "gpih-kyoto-1745-1754-bundle"
