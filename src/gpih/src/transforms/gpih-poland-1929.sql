-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "Capitalists and liberal professions" AS "capitalists_and_liberal_professions",
    "2.2" AS "2_2",
    "570",
    "3900",
    "c4",
    "Peasants; very small landholders" AS "peasants_very_small_landholders",
    "18767",
    "525",
    "63.71846670967304" AS "63_71846670967304"
FROM "gpih-poland-1929"
