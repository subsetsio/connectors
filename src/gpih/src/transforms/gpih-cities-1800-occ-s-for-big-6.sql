-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "officials",
    "9",
    "86",
    "0.026100151745068287" AS 0_026100151745068287,
    "9_2",
    "0",
    "0_2",
    "86_2",
    "86_3",
    "c9",
    "c10",
    "c11",
    "officials_2",
    "9_3",
    "86_4",
    "0.023529411764705882" AS 0_023529411764705882,
    "0_3",
    "0_4"
FROM "gpih-cities-1800-occ-s-for-big-6"
