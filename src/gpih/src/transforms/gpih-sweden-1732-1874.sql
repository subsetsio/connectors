-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS "sheet",
    "c0",
    "Kronor per" AS "kronor_per",
    "grams of Ag" AS "grams_of_ag",
    "kroner",
    "grams of Ag_2" AS "grams_of_ag_2",
    "kronor per_1" AS "kronor_per_1",
    "grams of Ag_3" AS "grams_of_ag_3",
    "kronor per_2" AS "kronor_per_2",
    "grams of Ag_4" AS "grams_of_ag_4",
    "Kronor" AS "kronor",
    "grams of Ag_5" AS "grams_of_ag_5",
    "Kronor_2" AS "kronor_2",
    "grams of Ag_6" AS "grams_of_ag_6",
    "Kronor_3" AS "kronor_3",
    "grams of Ag_7" AS "grams_of_ag_7",
    "Kronor_4" AS "kronor_4",
    "grams of Ag_8" AS "grams_of_ag_8"
FROM "gpih-sweden-1732-1874"
