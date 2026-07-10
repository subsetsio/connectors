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
    "Zipcode" AS zipcode,
    "Phone" AS phone,
    "Clinic Status" AS clinic_status,
    "Topic" AS topic,
    "SubTopic" AS subtopic,
    "Data_Value" AS data_value,
    CAST("ClinicId" AS BIGINT) AS clinicid,
    "TopicId" AS topicid,
    "SubTopicId" AS subtopicid,
    "Geolocation" AS geolocation
FROM "cdc-ix4g-rt8v"
