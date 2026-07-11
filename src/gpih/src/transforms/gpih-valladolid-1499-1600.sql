-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS sheet,
    "Commodity:" AS commodity,
    "Wheat" AS wheat,
    "Barley" AS barley,
    "Wine" AS wine,
    "Mutton" AS mutton,
    "Wheat_2" AS wheat_2,
    "Barley_2" AS barley_2,
    "Wine_2" AS wine_2,
    "Mutton_2" AS mutton_2,
    "Silver grams" AS silver_grams,
    "Wheat_3" AS wheat_3,
    "Barley_3" AS barley_3,
    "Wine_3" AS wine_3,
    "Mutton_3" AS mutton_3,
    "Vineyard" AS vineyard,
    "Vine" AS vine,
    "Grape" AS grape,
    "Vineyard_2" AS vineyard_2,
    "Vine_2" AS vine_2,
    "Grape_2" AS grape_2
FROM "gpih-valladolid-1499-1600"
