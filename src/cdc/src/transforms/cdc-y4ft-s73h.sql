-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "Locationabbr" AS locationabbr,
    "Locationdesc" AS locationdesc,
    "Class" AS class,
    "Topic" AS topic,
    "Question" AS question,
    "Response" AS response,
    "Break_Out" AS break_out,
    "Break_Out_Category" AS break_out_category,
    CAST("Sample_Size" AS BIGINT) AS sample_size,
    CAST("Data_value" AS DOUBLE) AS data_value,
    CAST("Confidence_limit_Low" AS DOUBLE) AS confidence_limit_low,
    CAST("Confidence_limit_High" AS DOUBLE) AS confidence_limit_high,
    CAST("Display_order" AS BIGINT) AS display_order,
    "Data_value_unit" AS data_value_unit,
    "Data_value_type" AS data_value_type,
    "Data_Value_Footnote_Symbol" AS data_value_footnote_symbol,
    "Data_Value_Footnote" AS data_value_footnote,
    "DataSource" AS datasource,
    "ClassId" AS classid,
    "TopicId" AS topicid,
    "LocationID" AS locationid,
    "BreakoutID" AS breakoutid,
    "BreakOutCategoryID" AS breakoutcategoryid,
    "QuestionID" AS questionid,
    "ResponseID" AS responseid,
    "GeoLocation" AS geolocation
FROM "cdc-y4ft-s73h"
