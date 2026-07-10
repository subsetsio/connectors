-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "StateAbbr" AS stateabbr,
    "StateDesc" AS statedesc,
    "CountyName" AS countyname,
    "CountyFIPS" AS countyfips,
    "LocationName" AS locationname,
    "DataSource" AS datasource,
    "Category" AS category,
    "Measure" AS measure,
    "Data_Value_Unit" AS data_value_unit,
    "Data_Value_Type" AS data_value_type,
    CAST("Data_Value" AS DOUBLE) AS data_value,
    CAST("MOE" AS DOUBLE) AS moe,
    CAST("TotalPopulation" AS BIGINT) AS totalpopulation,
    "LocationID" AS locationid,
    "CategoryID" AS categoryid,
    "MeasureID" AS measureid,
    "DataValueTypeID" AS datavaluetypeid,
    "Short_Question_Text" AS short_question_text,
    "Geolocation" AS geolocation
FROM "cdc-e539-uadk"
