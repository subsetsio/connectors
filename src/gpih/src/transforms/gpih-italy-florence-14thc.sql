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
    "Barley" AS barley,
    "Millet" AS millet,
    "Wine" AS wine,
    "Goat" AS goat,
    "Meat" AS meat,
    "Chicken" AS chicken,
    "Eggs" AS eggs,
    "Oil" AS oil,
    "Wheat_2" AS wheat_2,
    "Barley_2" AS barley_2,
    "Millet_2" AS millet_2,
    "Wine_2" AS wine_2,
    "Goat_2" AS goat_2,
    "Meat_2" AS meat_2,
    "Chicken_2" AS chicken_2,
    "Eggs_2" AS eggs_2,
    "Oil_2" AS oil_2,
    "Wheat_3" AS wheat_3,
    "Barley_3" AS barley_3,
    "Millet_3" AS millet_3,
    "Wine_3" AS wine_3,
    "Goat_3" AS goat_3,
    "Meat_3" AS meat_3,
    "Chicken_3" AS chicken_3,
    "Eggs_3" AS eggs_3,
    "Oil_3" AS oil_3,
    "1286-88" AS 1286_88,
    "4.6" AS 4_6,
    "c2",
    "0.4063333333333333" AS 0_4063333333333333,
    "Year" AS year,
    "soldi",
    "Florin" AS florin,
    "per soldi" AS per_soldi,
    "per denari" AS per_denari,
    "per libra de Firenze" AS per_libra_de_firenze
FROM "gpih-italy-florence-14thc"
