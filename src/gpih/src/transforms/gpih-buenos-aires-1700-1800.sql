-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "Commodity:" AS commodity,
    "Wheat" AS wheat,
    "c2",
    "c3",
    "Wheat_2" AS wheat_2,
    "c5",
    "Wheat_3" AS wheat_3,
    "Cow" AS cow,
    "Beef" AS beef,
    "Beef_2" AS beef_2,
    "Wine" AS wine,
    "Wine_2" AS wine_2,
    "Wine_3" AS wine_3,
    "Salt" AS salt,
    "Salt_2" AS salt_2,
    "Salt_3" AS salt_3,
    "Lard" AS lard,
    "Wood" AS wood,
    "Paper" AS paper,
    "Lard_2" AS lard_2,
    "Wood_2" AS wood_2,
    "Paper_2" AS paper_2,
    "Lard_3" AS lard_3,
    "Wood_3" AS wood_3,
    "Paper_3" AS paper_3
FROM "gpih-buenos-aires-1700-1800"
