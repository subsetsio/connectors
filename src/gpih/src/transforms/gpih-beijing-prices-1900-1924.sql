-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS "sheet",
    "Physical unit" AS "physical_unit",
    "100 catties" AS "100_catties",
    "100 catties_2" AS "100_catties_2",
    "100 catties_3" AS "100_catties_3",
    "100 catties_4" AS "100_catties_4",
    "100 catties_5" AS "100_catties_5",
    "100 catties_6" AS "100_catties_6",
    "100 catties_7" AS "100_catties_7",
    "kg." AS "kg",
    "kg._2" AS "kg_2",
    "kg._3" AS "kg_3",
    "kg._4" AS "kg_4",
    "kg._5" AS "kg_5",
    "kg._6" AS "kg_6",
    "kg._7" AS "kg_7"
FROM "gpih-beijing-prices-1900-1924"
