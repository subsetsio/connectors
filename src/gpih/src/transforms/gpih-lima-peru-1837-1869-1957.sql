-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "Market foods" AS "market_foods",
    "4986",
    "34.97720098211154" AS "34_97720098211154",
    "Meats" AS "meats",
    "460",
    "Meat" AS "meat",
    "34.25" AS "34_25",
    "(Meat)" AS "meat_2",
    "18.6" AS "18_6",
    "34.12844036697248" AS "34_12844036697248",
    "All Food" AS "all_food",
    "55.61" AS "55_61",
    "c2",
    "47.04" AS "47_04"
FROM "gpih-lima-peru-1837-1869-1957"
