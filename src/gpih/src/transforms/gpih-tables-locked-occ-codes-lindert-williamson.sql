-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS sheet,
    "Code" AS code,
    "Class" AS class,
    "Occupation" AS occupation,
    "c3",
    "Code_2" AS code_2,
    "Class_2" AS class_2,
    "Occupation_2" AS occupation_2
FROM "gpih-tables-locked-occ-codes-lindert-williamson"
