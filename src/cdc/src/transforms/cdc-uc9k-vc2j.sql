-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "LocationID" AS locationid,
    "Year" AS year,
    "LocationAbbr" AS locationabbr,
    "LocationDesc" AS locationdesc,
    "GeographicLevel" AS geographiclevel,
    "DataSource" AS datasource,
    "Class" AS class,
    "Topic" AS topic,
    CAST("Data_Value" AS DOUBLE) AS data_value,
    "Data_Value_Unit" AS data_value_unit,
    "Data_Value_Type" AS data_value_type,
    "Data_Value_Footnote_Symbol" AS data_value_footnote_symbol,
    "Data_Value_Footnote" AS data_value_footnote,
    CAST("Confidence_limit_Low" AS DOUBLE) AS confidence_limit_low,
    CAST("Confidence_limit_High" AS DOUBLE) AS confidence_limit_high,
    "StratificationCategory1" AS stratificationcategory1,
    "Stratification1" AS stratification1,
    "StratificationCategory2" AS stratificationcategory2,
    "Stratification2" AS stratification2,
    "StratificationCategory3" AS stratificationcategory3,
    "Stratification3" AS stratification3,
    "TopicID" AS topicid,
    CAST("X_long" AS DOUBLE) AS x_long,
    CAST("Y_lat" AS DOUBLE) AS y_lat
FROM "cdc-uc9k-vc2j"
