-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "c0",
    "Czeladnik" AS czeladnik,
    "Czeladnik_2" AS czeladnik_2,
    "Robotnik" AS robotnik,
    "1412",
    "9.5" AS 9_5,
    "4",
    "1517",
    "591.36" AS 591_36,
    "665.28" AS 665_28,
    "1617",
    "1617_2",
    "739.2" AS 739_2,
    "184.8" AS 184_8,
    "110.88" AS 110_88,
    "147.84" AS 147_84,
    "110.88_2" AS 110_88_2,
    "147.84_2" AS 147_84_2,
    "92.4" AS 92_4,
    "c12",
    "147.8" AS 147_8,
    "110.9" AS 110_9,
    "110.9_2" AS 110_9_2,
    "110.9_3" AS 110_9_3,
    "92.4_2" AS 92_4_2,
    "110.9_4" AS 110_9_4,
    "120.1" AS 120_1,
    "1517_2",
    "1045.9679999999998" AS 1045_9679999999998,
    "129.36" AS 129_36,
    "114.84285714285714" AS 114_84285714285714,
    "409.44875" AS 409_44875,
    "Year" AS year,
    "in platea s. Joannis" AS in_platea_s_joannis,
    "Podelwie I" AS podelwie_i,
    "s. Stefani" AS s_stefani
FROM "gpih-krakow-w-s-int-realty-1393-1600"
