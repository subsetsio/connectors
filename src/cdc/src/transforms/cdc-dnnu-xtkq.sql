-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("YearStart" AS BIGINT) AS yearstart,
    CAST("YearEnd" AS BIGINT) AS yearend,
    "LocationAbbr" AS locationabbr,
    "LocationDesc" AS locationdesc,
    "Datasource" AS datasource,
    "Class" AS class,
    "Topic" AS topic,
    "Question" AS question,
    "Data_Value_Unit" AS data_value_unit,
    "Data_Value_Type" AS data_value_type,
    CAST("Data_Value" AS DOUBLE) AS data_value,
    CAST("Data_Value_Alt" AS DOUBLE) AS data_value_alt,
    "Data_Value_Footnote_Symbol" AS data_value_footnote_symbol,
    "Data_Value_Footnote" AS data_value_footnote,
    CAST("Low_Confidence_Limit" AS DOUBLE) AS low_confidence_limit,
    CAST("High_Confidence_Limit" AS DOUBLE) AS high_confidence_limit,
    CAST("Sample_Size" AS BIGINT) AS sample_size,
    "Total" AS total,
    "Sex" AS sex,
    "Race\Ethnicity" AS race_ethnicity,
    "GeoLocation" AS geolocation,
    "ClassID" AS classid,
    "TopicID" AS topicid,
    "QuestionID" AS questionid,
    "DataValueTypeID" AS datavaluetypeid,
    "LocationID" AS locationid,
    "StratificationCategory1" AS stratificationcategory1,
    "Stratification1" AS stratification1,
    "StratificationCategoryId1" AS stratificationcategoryid1,
    "StratificationID1" AS stratificationid1
FROM "cdc-dnnu-xtkq"
