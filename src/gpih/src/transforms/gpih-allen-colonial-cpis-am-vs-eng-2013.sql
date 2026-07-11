-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "c0",
    "MA" AS ma,
    "Philadelphia" AS philadelphia,
    "c3",
    "c4",
    "England" AS england,
    "S. Engl." AS s_engl,
    "£ sterling" AS sterling,
    "MA_2" AS ma_2,
    "Philadelphia_2" AS philadelphia_2,
    "c10",
    "England_2" AS england_2,
    "c12",
    "c13",
    "c14",
    "c15",
    "Philly/" AS philly,
    "Chesapeake/" AS chesapeake,
    "1631",
    "4.68022882053552" AS 4_68022882053552,
    "3.833160348126805" AS 3_833160348126805,
    "1.7265749324475599" AS 1_7265749324475599,
    "c5",
    "Massachusetts" AS massachusetts,
    "Chesapeake" AS chesapeake_2,
    "c11"
FROM "gpih-allen-colonial-cpis-am-vs-eng-2013"
