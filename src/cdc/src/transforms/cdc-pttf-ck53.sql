-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "LocationAbbr" AS locationabbr,
    "LocationDesc" AS locationdesc,
    "Topic" AS topic,
    "Question" AS question,
    "DataSource" AS datasource,
    "Response" AS response,
    "Data_Value_Unit" AS data_value_unit,
    "Data_Value_Type" AS data_value_type,
    CAST("Data_Value" AS DOUBLE) AS data_value,
    "Data_Value_Footnote_Symbol" AS data_value_footnote_symbol,
    "Data_Value_Footnote" AS data_value_footnote,
    CAST("Low_Confidence_limit" AS DOUBLE) AS low_confidence_limit,
    CAST("High_Confidence_Limit" AS DOUBLE) AS high_confidence_limit,
    CAST("Sample_Size" AS BIGINT) AS sample_size,
    "Break_Out" AS break_out,
    "Break_Out_Category" AS break_out_category,
    "GeoLocation" AS geolocation,
    "TopicId" AS topicid,
    "QuestionId" AS questionid,
    CAST("LocationId" AS BIGINT) AS locationid,
    "BreakOutId" AS breakoutid,
    "BreakOutCategoryId" AS breakoutcategoryid,
    "ResponseId" AS responseid,
    "Geographic Level" AS geographic_level
FROM "cdc-pttf-ck53"
