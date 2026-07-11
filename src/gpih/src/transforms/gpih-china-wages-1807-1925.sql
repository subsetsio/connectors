-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "1900",
    "23.6" AS "23_6",
    "0.16992000000000002" AS "0_16992000000000002",
    "6.28704" AS "6_28704",
    "2.923" AS "2_923",
    "2.150886075949367" AS "2_150886075949367",
    "1807",
    "81",
    "979",
    "0.083" AS "0_083",
    "3.071" AS "3_071",
    "1875",
    "0.027" AS "0_027",
    "0.033" AS "0_033",
    "0.999" AS "0_999",
    "1.221" AS "1_221",
    "1912",
    "0.275" AS "0_275",
    "7.3260000000000005" AS "7_3260000000000005"
FROM "gpih-china-wages-1807-1925"
