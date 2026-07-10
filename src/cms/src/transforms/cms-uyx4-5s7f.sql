-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Facility ID" AS facility_id,
    "Facility Name" AS facility_name,
    "Address" AS address,
    "City/Town" AS city_town,
    "State" AS state,
    "ZIP Code" AS zip_code,
    "County/Parish" AS county_parish,
    "Telephone Number" AS telephone_number,
    "Hospital Type" AS hospital_type,
    "Hospital Ownership" AS hospital_ownership,
    "Emergency Services" AS emergency_services,
    "Hospital overall rating" AS hospital_overall_rating,
    "Hospital overall rating footnote" AS hospital_overall_rating_footnote
FROM "cms-uyx4-5s7f"
