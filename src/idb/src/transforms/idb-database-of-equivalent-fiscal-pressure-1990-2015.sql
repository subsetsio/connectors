-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Country_ES" AS country_es,
    "Country_EN" AS country_en,
    "Indicator_Level1_ES" AS indicator_level1_es,
    "Indicator_Level1_EN" AS indicator_level1_en,
    "Indicator_Level2_ES" AS indicator_level2_es,
    "Indicator_Level2_EN" AS indicator_level2_en,
    "Indicator_Level3_ES" AS indicator_level3_es,
    "Indicator_Level3_EN" AS indicator_level3_en,
    "Indicator_Level4_ES" AS indicator_level4_es,
    "Indicator_Level4_EN" AS indicator_level4_en,
    "Indicator_ES" AS indicator_es,
    "Indicator_EN" AS indicator_en,
    "Year_Date" AS year_date,
    CAST("Year_Text" AS BIGINT) AS year_text,
    CAST("Value" AS DOUBLE) AS value,
    "Unit_ES" AS unit_es,
    "Unit_EN" AS unit_en,
    "source_resource"
FROM "idb-database-of-equivalent-fiscal-pressure-1990-2015"
