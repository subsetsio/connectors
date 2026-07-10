-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "WHO_Region" AS who_region,
    "Datasource" AS datasource,
    "Country" AS country,
    "SurveySite" AS surveysite,
    "Topic" AS topic,
    "Mpower" AS mpower,
    "Indicator" AS indicator,
    "Data_Value_Type" AS data_value_type,
    "Data_Value_Unit" AS data_value_unit,
    CAST("Data_Value" AS DOUBLE) AS data_value,
    "Data_Value_Footnote_Symbol" AS data_value_footnote_symbol,
    "Data_Value_Footnote" AS data_value_footnote,
    CAST("Low_Confidence_Limit" AS DOUBLE) AS low_confidence_limit,
    CAST("High_Confidence_Limit" AS DOUBLE) AS high_confidence_limit,
    CAST("Sample_Size" AS BIGINT) AS sample_size,
    "Discipline" AS discipline,
    "Sex" AS sex,
    "Geolocation" AS geolocation,
    "RegionAbbr" AS regionabbr,
    "CountryAbbr" AS countryabbr,
    "SurveySiteAbbr" AS surveysiteabbr,
    CAST("LocationID" AS BIGINT) AS locationid,
    "TopicID" AS topicid,
    "MpowerID" AS mpowerid,
    "IndicatorID" AS indicatorid,
    "StratificationID1" AS stratificationid1,
    "DataValueTypeID" AS datavaluetypeid
FROM "cdc-x6ag-8y7r"
