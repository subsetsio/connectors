-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS sheet,
    "Beans/peas" AS beans_peas,
    "15 kg" AS 15_kg,
    "1.053" AS 1_053,
    "4.1" AS 4_1,
    "139",
    "9"
FROM "gpih-beijing-1745-1754-bundle"
