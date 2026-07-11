-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "c0",
    "Commodity:" AS "commodity",
    "Grains" AS "grains",
    "Grains_2" AS "grains_2",
    "Grains_3" AS "grains_3",
    "Grains_4" AS "grains_4",
    "Grains_5" AS "grains_5",
    "Grains_6" AS "grains_6",
    "Grains_7" AS "grains_7",
    "Grains_8" AS "grains_8",
    "Grains_9" AS "grains_9",
    "Occupation:" AS "occupation",
    "Bricklayer" AS "bricklayer",
    "Laborer" AS "laborer",
    "Laborer_2" AS "laborer_2",
    "Laborer_3" AS "laborer_3",
    "Agricultural Laborer" AS "agricultural_laborer",
    "Bricklayer_2" AS "bricklayer_2",
    "Laborer_4" AS "laborer_4",
    "Laborer_5" AS "laborer_5",
    "Laborer_6" AS "laborer_6",
    "Agricultural Laborer_2" AS "agricultural_laborer_2",
    "Bricklayer_3" AS "bricklayer_3",
    "Laborer_7" AS "laborer_7",
    "Laborer_8" AS "laborer_8",
    "Laborer_9" AS "laborer_9",
    "Agricultural Laborer_3" AS "agricultural_laborer_3",
    "Monetary Unit:" AS "monetary_unit",
    "Silver grams" AS "silver_grams",
    "Silver grams_2" AS "silver_grams_2",
    "Silver grams_3" AS "silver_grams_3",
    "Silver grams_4" AS "silver_grams_4"
FROM "gpih-italy-north-1285-1850"
