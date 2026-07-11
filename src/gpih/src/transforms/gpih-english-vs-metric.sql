-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "0.032151 troy ounces =" AS "0_032151_troy_ounces",
    "c1",
    "1 gram" AS "1_gram",
    "1 barrel of wheat = 88.904 kg" AS "1_barrel_of_wheat_88_904_kg",
    "c4",
    "c5",
    "c6",
    "c7"
FROM "gpih-english-vs-metric"
