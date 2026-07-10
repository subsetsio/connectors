-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "Question" AS question,
    "Area" AS area,
    "Area_abbr" AS area_abbr,
    "Demographics_Type" AS demographics_type,
    "Demographics_Value" AS demographics_value,
    "Percent" AS percent,
    "Low_Confidence_Interval" AS low_confidence_interval,
    "High_Confidence_Interval" AS high_confidence_interval,
    "Confidence_Interval_Formatted" AS confidence_interval_formatted,
    "Data_Label" AS data_label,
    "Percentile_Range" AS percentile_range
FROM "cdc-5eh7-pjx8"
