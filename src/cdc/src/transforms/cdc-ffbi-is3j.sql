-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "LocationAbbr" AS locationabbr,
    "LocationDesc" AS locationdesc,
    CAST("Year" AS BIGINT) AS year,
    "Topic" AS topic,
    "Indicator" AS indicator,
    "SubMeasure" AS submeasure,
    CAST("Amount" AS DOUBLE) AS amount,
    "Data_Value_Unit" AS data_value_unit,
    "Data_Value_Footnote_Symbol" AS data_value_footnote_symbol,
    "Data_Value_Footnote" AS data_value_footnote,
    "GeoLocation" AS geolocation,
    "TopicTypeId" AS topictypeid,
    "TopicId" AS topicid,
    "MeasureId" AS measureid,
    "Source" AS source,
    "SubMeasureID" AS submeasureid,
    CAST("DisplayOrder" AS BIGINT) AS displayorder
FROM "cdc-ffbi-is3j"
