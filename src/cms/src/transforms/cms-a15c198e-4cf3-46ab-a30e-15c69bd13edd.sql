-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Name of Initiative" AS name_of_initiative,
    "Organization Name" AS organization_name,
    "Location Name" AS location_name,
    "Location 1" AS location_1,
    "Street Address Line 1" AS street_address_line_1,
    "Street Address Line 2" AS street_address_line_2,
    "City" AS city,
    "State" AS state,
    CAST("ZIP Code" AS BIGINT) AS zip_code,
    "Telephone Number" AS telephone_number,
    CAST("NPI" AS BIGINT) AS npi,
    "Category" AS category,
    CAST("Unique ID" AS BIGINT) AS unique_id
FROM "cms-a15c198e-4cf3-46ab-a30e-15c69bd13edd"
