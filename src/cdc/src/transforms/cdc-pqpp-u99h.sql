-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "StateAbbr" AS stateabbr,
    "StateDesc" AS statedesc,
    "LocationName" AS locationname,
    "DataSource" AS datasource,
    "Category" AS category,
    "Measure" AS measure,
    "Data_Value_Unit" AS data_value_unit,
    "Data_Value_Type" AS data_value_type,
    CAST("Data_Value" AS DOUBLE) AS data_value,
    "Data_Value_Footnote_Symbol" AS data_value_footnote_symbol,
    "Data_Value_Footnote" AS data_value_footnote,
    CAST("Low_Confidence_Limit" AS DOUBLE) AS low_confidence_limit,
    CAST("High_Confidence_Limit" AS DOUBLE) AS high_confidence_limit,
    CAST("TotalPopulation" AS BIGINT) AS totalpopulation,
    "LocationID" AS locationid,
    "CategoryID" AS categoryid,
    "MeasureId" AS measureid,
    "DataValueTypeID" AS datavaluetypeid,
    "Short_Question_Text" AS short_question_text,
    "Geolocation" AS geolocation
FROM "cdc-pqpp-u99h"
