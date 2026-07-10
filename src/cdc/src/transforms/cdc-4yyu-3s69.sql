-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "LocationAbbr" AS locationabbr,
    "LocationDesc" AS locationdesc,
    "DataSource" AS datasource,
    "TopicType" AS topictype,
    "TopicDesc" AS topicdesc,
    "MeasureDesc" AS measuredesc,
    "Data_Value_Unit" AS data_value_unit,
    "Data_Value_Type" AS data_value_type,
    CAST("Data_Value" AS BIGINT) AS data_value,
    "Data_Value_Footnote_Symbol" AS data_value_footnote_symbol,
    "Data_Value_Footnote" AS data_value_footnote,
    "Sex" AS sex,
    "GeoLocation" AS geolocation,
    "TopicTypeID" AS topictypeid,
    "TopicID" AS topicid,
    "MeasureID" AS measureid,
    "SubMeasureID" AS submeasureid,
    "DisplayOrder" AS displayorder
FROM "cdc-4yyu-3s69"
