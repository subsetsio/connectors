-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS "sheet",
    "Currency" AS "currency",
    "£ 1000s" AS "1000s",
    "£ 1000s_2" AS "1000s_2",
    "£ 1000s_3" AS "1000s_3",
    "£ 1000s_4" AS "1000s_4",
    "£ 1000s_5" AS "1000s_5",
    "£ 1000s_6" AS "1000s_6",
    "£ 1000s_7" AS "1000s_7",
    "£ 1000s_8" AS "1000s_8",
    "£ 1000s_9" AS "1000s_9",
    "£ 1000s_10" AS "1000s_10",
    "£ 1000s_11" AS "1000s_11",
    "£ 1000s_12" AS "1000s_12",
    "£ 1000s_13" AS "1000s_13",
    "£ 1000s_14" AS "1000s_14",
    "£ 1000s_15" AS "1000s_15",
    "£ 1000s_16" AS "1000s_16",
    "£ 1000s_17" AS "1000s_17",
    "£ 1000s_18" AS "1000s_18",
    "£ 1000s_19" AS "1000s_19",
    "£ 1000s_20" AS "1000s_20",
    "£ 1000s_21" AS "1000s_21",
    "£ 1000s_22" AS "1000s_22",
    "£ 1000s_23" AS "1000s_23",
    "£ 1000s_24" AS "1000s_24",
    "£ 1000s_25" AS "1000s_25",
    "£ 1000s_26" AS "1000s_26",
    "£ 1000s_27" AS "1000s_27",
    "£ 1000s_28" AS "1000s_28",
    "£ 1000s_29" AS "1000s_29",
    "£ 1000s_30" AS "1000s_30",
    "£ 1000s_31" AS "1000s_31",
    "£ 1000s_32" AS "1000s_32",
    "£ 1000s_33" AS "1000s_33",
    "£ 1000s_34" AS "1000s_34",
    "£ 1000s_35" AS "1000s_35"
FROM "gpih-frankema-revenues-british-empire"
