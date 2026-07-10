-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "StateAbbr" AS stateabbr,
    "LocationAbbr" AS locationabbr,
    "LocationDesc" AS locationdesc,
    "Category" AS category,
    "Indicator" AS indicator,
    "ShortIndicatorText" AS shortindicatortext,
    "Type" AS type,
    "DataSource" AS datasource,
    "Data_Value_Unit" AS data_value_unit,
    "Data_Value_Type" AS data_value_type,
    CAST("Data_Value" AS BIGINT) AS data_value,
    "Data_Value_Footnote_Symbol" AS data_value_footnote_symbol,
    "Data_Value_Footnote_Text" AS data_value_footnote_text,
    "Geolocation" AS geolocation,
    "Break_Out_Category1" AS break_out_category1,
    "Break_Out1" AS break_out1,
    CAST("LocationID" AS BIGINT) AS locationid,
    "TypeID" AS typeid,
    "Break_Out1_ID" AS break_out1_id,
    "IndicatorID" AS indicatorid,
    CAST("MWF_Participant" AS BOOLEAN) AS mwf_participant,
    "IndicatorGroupId" AS indicatorgroupid,
    "TopicId" AS topicid
FROM "cdc-hgyx-uuxz"
