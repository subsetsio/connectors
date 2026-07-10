-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "LocationAbbr" AS locationabbr,
    "LocationDesc" AS locationdesc,
    "GeographicLevel" AS geographiclevel,
    "DataSource" AS datasource,
    "Class" AS class,
    "Topic" AS topic,
    "Data_Value" AS data_value,
    "Data_Value_Unit" AS data_value_unit,
    "Data_Value_Type" AS data_value_type,
    "Data_Value_Footnote_Symbol" AS data_value_footnote_symbol,
    "Data_Value_Footnote" AS data_value_footnote,
    "Confidence_limit_Low" AS confidence_limit_low,
    "Confidence_limit_High" AS confidence_limit_high,
    "StratificationCategory1" AS stratificationcategory1,
    "Stratification1" AS stratification1,
    "StratificationCategory2" AS stratificationcategory2,
    "Stratification2" AS stratification2,
    "StratificationCategory3" AS stratificationcategory3,
    "Stratification3" AS stratification3,
    "LocationID" AS locationid
FROM "cdc-7b9s-s8ck"
