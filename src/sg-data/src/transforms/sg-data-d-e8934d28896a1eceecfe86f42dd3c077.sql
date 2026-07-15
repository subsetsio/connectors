-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Postal_Code" AS postal_code,
    "Building_Name" AS building_name,
    "Location_Description" AS location_description
FROM "sg-data-d-e8934d28896a1eceecfe86f42dd3c077"
