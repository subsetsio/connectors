-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "Enrollment ID" AS enrollment_id,
    "Legal Business Name" AS legal_business_name,
    "Street Address Line 1" AS street_address_line_1,
    "Street Address Line 2" AS street_address_line_2,
    "City" AS city,
    "State" AS state,
    "ZIP Code" AS zip_code,
    "Practice Location Phone Number" AS practice_location_phone_number,
    "Specialty Name" AS specialty_name,
    "Geographic Location Type Description" AS geographic_location_type_description,
    "Geographic Location City Name" AS geographic_location_city_name,
    "Geographic Location State Code" AS geographic_location_state_code,
    "Geographic Location ZIP Code" AS geographic_location_zip_code,
    "State County Name" AS state_county_name
FROM "cms-31f25ab6-2fe3-4bad-ac5a-90635ed79935"
