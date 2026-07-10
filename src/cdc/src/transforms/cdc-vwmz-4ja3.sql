-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "LocationAbbr" AS locationabbr,
    "LocationDesc" AS locationdesc,
    "DataSource" AS datasource,
    "Class" AS class,
    "Topic" AS topic,
    "Question" AS question,
    "Response" AS response,
    "Data_Value_Unit" AS data_value_unit,
    "Data_Value_Type" AS data_value_type,
    "Data_Value" AS data_value,
    CAST("Data_Value_Alt" AS BIGINT) AS data_value_alt,
    "Data_Value_Footnote_Symbol" AS data_value_footnote_symbol,
    "Data_Value_Footnote" AS data_value_footnote,
    "Low_Confidence_Limit" AS low_confidence_limit,
    "High_Confidence_Limit" AS high_confidence_limit,
    "Sample_Size" AS sample_size,
    "Break_Out" AS break_out,
    "Break_Out_Category" AS break_out_category,
    "GeoLocation" AS geolocation,
    "ClassID" AS classid,
    "TopicID" AS topicid,
    "QuestionID" AS questionid,
    "ResponseID" AS responseid,
    "LocationID" AS locationid,
    "BreakOutID" AS breakoutid,
    "BreakOutCategoryID" AS breakoutcategoryid,
    "Data_Value_Category" AS data_value_category,
    "Data_Value_Category_ID" AS data_value_category_id
FROM "cdc-vwmz-4ja3"
