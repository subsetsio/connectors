-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "LocationAbbr" AS locationabbr,
    "LocationDesc" AS locationdesc,
    "Category" AS category,
    "Indicator" AS indicator,
    "Response" AS response,
    "Datasource" AS datasource,
    "Data_Value_Unit" AS data_value_unit,
    "Data_Value_Type" AS data_value_type,
    CAST("Data_Value" AS DOUBLE) AS data_value,
    "Data_Value_Footnote_Symbol" AS data_value_footnote_symbol,
    "Data_Value_Footnote" AS data_value_footnote,
    CAST("High_Confidence_Interval" AS DOUBLE) AS high_confidence_interval,
    CAST("Low_Confidence_Interval" AS DOUBLE) AS low_confidence_interval,
    CAST("SampleSize" AS BIGINT) AS samplesize,
    "Break_Out" AS break_out,
    "LocationID" AS locationid,
    "GeoLocation" AS geolocation,
    CAST("SortUSFirst" AS BIGINT) AS sortusfirst,
    "Break_Out_Category" AS break_out_category,
    "Break_Out_ID" AS break_out_id,
    CAST("SortBreakOutID" AS BIGINT) AS sortbreakoutid,
    "IndicatorID" AS indicatorid
FROM "cdc-jz6n-v26y"
