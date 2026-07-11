-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "c0",
    "(thousands)" AS "thousands",
    "Per capita" AS "per_capita",
    "Size" AS "size",
    "(thousands)_2" AS "thousands_2",
    "Per capita_2" AS "per_capita_2",
    "Size_2" AS "size_2",
    "(thousands)_3" AS "thousands_3",
    "Per capita_3" AS "per_capita_3",
    "Size_3" AS "size_3",
    "(thousands)_4" AS "thousands_4",
    "Per capita_4" AS "per_capita_4",
    "Size_4" AS "size_4",
    "income",
    "mid-point" AS "mid_point",
    "recipients",
    "population",
    "income_2",
    "income per" AS "income_per",
    "income per_2" AS "income_per_2",
    "recipients_2",
    "population_2",
    "income_3",
    "income per_3" AS "income_per_3",
    "income per_4" AS "income_per_4",
    "c12",
    "c13"
FROM "gpih-java-1924-with-foreigners"
