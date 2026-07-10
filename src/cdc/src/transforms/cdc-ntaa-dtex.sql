-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    CAST("Quarter" AS BIGINT) AS quarter,
    "LocationAbbr" AS locationabbr,
    "LocationDesc" AS locationdesc,
    "TopicType" AS topictype,
    "Topic" AS topic,
    "MeasureDesc" AS measuredesc,
    "Sub_Measure" AS sub_measure,
    "Fee-For-Service Plans" AS fee_for_service_plans,
    CAST("Fee-For-Service_Plans_AltValue" AS BIGINT) AS fee_for_service_plans_altvalue,
    "Managed Care Plans" AS managed_care_plans,
    CAST("Managed Care Plans_AltValue" AS BIGINT) AS managed_care_plans_altvalue,
    "Summary" AS summary,
    CAST("Summary_AltValue" AS BIGINT) AS summary_altvalue,
    "Data_Value_Footnote_Symbol" AS data_value_footnote_symbol,
    "Data_Value_Footnote" AS data_value_footnote,
    "DataSource" AS datasource,
    "GeoLocation" AS geolocation,
    "TopicTypeId" AS topictypeid,
    "TopicId" AS topicid,
    "MeasureId" AS measureid,
    "SubMeasureID" AS submeasureid,
    CAST("DisplayOrder" AS BIGINT) AS displayorder
FROM "cdc-ntaa-dtex"
