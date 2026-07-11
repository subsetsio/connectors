-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "Year" AS "year",
    "Ghee" AS "ghee",
    "Oil" AS "oil",
    "Sugar" AS "sugar",
    "Salt" AS "salt",
    "Barley" AS "barley",
    "Wheat" AS "wheat",
    "Jowar" AS "jowar",
    "Bajra" AS "bajra",
    "Gram" AS "gram",
    "Rice" AS "rice",
    "c11",
    "c12",
    "c13",
    "c 1594" AS "c_1594",
    "c1",
    "2 dams" AS "2_dams",
    "6.78" AS "6_78",
    "4.52" AS "4_52",
    "5.42" AS "5_42",
    "9.04" AS "9_04",
    "6.78_2" AS "6_78_2",
    "2.71" AS "2_71",
    "7.266102239845676" AS "7_266102239845676",
    "4.844068159897116" AS "4_844068159897116",
    "5.808595005894331" AS "5_808595005894331",
    "9.688136319794232" AS "9_688136319794232",
    "7.266102239845676_2" AS "7_266102239845676_2",
    "2.9042975029471654" AS "2_9042975029471654",
    "1594",
    "Philip Khan July 2005" AS "philip_khan_july_2005",
    "PUNE REGION (INDIA)" AS "pune_region_india",
    "c3"
FROM "gpih-north-india-1600-1938-mukerjee"
