-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "Commodity" AS commodity,
    "Wheat" AS wheat,
    "Rice" AS rice,
    "Chickpeas" AS chickpeas,
    "Yerba" AS yerba,
    "Sugar" AS sugar,
    "Beans" AS beans,
    "Wine" AS wine,
    "Salted meat" AS salted_meat,
    "Wheat_2" AS wheat_2,
    "Rice_2" AS rice_2,
    "Chickpeas_2" AS chickpeas_2,
    "Yerba_2" AS yerba_2,
    "Sugar_2" AS sugar_2,
    "Beans_2" AS beans_2,
    "Wine_2" AS wine_2,
    "Salted meat_2" AS salted_meat_2,
    "Wheat_3" AS wheat_3,
    "Rice_3" AS rice_3,
    "Chickpeas_3" AS chickpeas_3,
    "Yerba_3" AS yerba_3,
    "Sugar_3" AS sugar_3,
    "Beans_3" AS beans_3,
    "Wine_3" AS wine_3,
    "Salted meat_3" AS salted_meat_3,
    "1770",
    "5.8" AS 5_8,
    "c2",
    "144.4664" AS 144_4664
FROM "gpih-buenos-aires-1770-1812"
