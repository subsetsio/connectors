-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS sheet,
    "Bread" AS bread,
    "182 kg" AS 182_kg,
    "0.693" AS 0_693,
    "28.9" AS 28_9,
    "1223",
    "50"
FROM "gpih-n-europe-1745-1754"
