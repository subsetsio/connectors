-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
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
    "StratificationCategory1" AS stratificationcategory1,
    "Stratification1" AS stratification1,
    "StratificationCategory2" AS stratificationcategory2,
    "Stratification2" AS stratification2,
    "TopicID" AS topicid,
    "LocationID" AS locationid,
    CAST("Y_lat" AS DOUBLE) AS y_lat,
    CAST("X_lon" AS DOUBLE) AS x_lon
FROM "cdc-th8y-thx5"
