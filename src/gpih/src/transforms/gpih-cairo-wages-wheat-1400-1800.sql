-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "South. England" AS "south_england",
    "2.6" AS "2_6",
    "2.92" AS "2_92",
    "3.68" AS "3_68",
    "5.71" AS "5_71",
    "9.2" AS "9_2"
FROM "gpih-cairo-wages-wheat-1400-1800"
