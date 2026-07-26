-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "geographical_district_code",
    "building_code",
    "ats_system_code",
    "location_name",
    "primary_address",
    "city",
    "zip",
    "service"
FROM "nyc-open-data-qxbt-vysj"
