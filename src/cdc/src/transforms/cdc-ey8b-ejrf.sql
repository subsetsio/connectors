-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "LocationAbbr" AS locationabbr,
    "LocationDesc" AS locationdesc,
    "FacilityName" AS facilityname,
    "MedicalDirector" AS medicaldirector,
    "Address" AS address,
    "City" AS city,
    "ZipCode" AS zipcode,
    "Phone" AS phone,
    "Clinic Status" AS clinic_status,
    "Type" AS type,
    "Topic" AS topic,
    "Question" AS question,
    "Filter" AS filter,
    "Breakout_Category" AS breakout_category,
    "Breakout" AS breakout,
    "Data_Value" AS data_value,
    CAST("Data_Value_num" AS DOUBLE) AS data_value_num,
    "Data_Value_Footnote_Symbol" AS data_value_footnote_symbol,
    "Data_Value_Footnote" AS data_value_footnote,
    CAST("Cycle_Count" AS BIGINT) AS cycle_count,
    CAST("ClinicId" AS BIGINT) AS clinicid,
    "TypeId" AS typeid,
    "TopicId" AS topicid,
    "QuestionId" AS questionid,
    "FilterId" AS filterid,
    "BreakOutCategoryId" AS breakoutcategoryid,
    "BreakOutId" AS breakoutid,
    "GeoLocation" AS geolocation
FROM "cdc-ey8b-ejrf"
