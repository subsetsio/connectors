-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS sheet,
    "Commodity:" AS commodity,
    "Flour" AS flour,
    "Corn" AS corn,
    "Rice" AS rice,
    "Wheat" AS wheat,
    "Flour_2" AS flour_2,
    "Corn_2" AS corn_2,
    "Rice_2" AS rice_2,
    "Wheat_2" AS wheat_2,
    "Wheat_3" AS wheat_3,
    "Flour_3" AS flour_3,
    "Corn_3" AS corn_3,
    "Rice_3" AS rice_3,
    "Wheat_4" AS wheat_4,
    "Wheat_5" AS wheat_5,
    "Firewood" AS firewood,
    "c2",
    "Firewood_2" AS firewood_2,
    """Meat""" AS meat,
    """Meat""_2" AS meat_2,
    """Meat""_3" AS meat_3,
    "Wine" AS wine,
    "Wine_2" AS wine_2,
    "Wine_3" AS wine_3,
    "Salt" AS salt,
    "Sugar" AS sugar,
    "Tobacco" AS tobacco,
    "Salt_2" AS salt_2,
    "Sugar_2" AS sugar_2,
    "Tobacco_2" AS tobacco_2,
    "Salt_3" AS salt_3,
    "Sugar_3" AS sugar_3,
    "Tobacco_3" AS tobacco_3,
    "Cotton Cloth" AS cotton_cloth,
    "Cotton Cloth_2" AS cotton_cloth_2,
    "Cotton Cloth_3" AS cotton_cloth_3
FROM "gpih-chile-1631-1830"
