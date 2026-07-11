-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "Laborers" AS laborers,
    "Farmers (both sexes)" AS farmers_both_sexes,
    "513277",
    "59976",
    "116.84918669646214" AS 116_84918669646214,
    "39.22654593754346" AS 39_22654593754346,
    "1026553.9999999999" AS 1026553_9999999999,
    "59976_2",
    "116.84918669646214_2" AS 116_84918669646214_2,
    "0.6477620539794462" AS 0_6477620539794462,
    "c10",
    "Female spinners" AS female_spinners,
    "59.00058410518662" AS 59_00058410518662,
    "335556",
    "c14",
    "c15",
    "c16",
    "c17",
    "c18",
    "c19",
    "c20",
    "c21",
    "c22",
    "c23",
    "c24"
FROM "gpih-peru-1876-rev-branko-31mar2016"
