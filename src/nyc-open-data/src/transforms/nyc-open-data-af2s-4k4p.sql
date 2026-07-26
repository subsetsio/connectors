-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dvs_res_id",
    "_name" AS name,
    "service",
    "_hours" AS hours,
    "phone_number",
    "address",
    "city",
    "state",
    "zip",
    "building_details",
    "borough",
    "walkin",
    "email_address",
    "website",
    "service_details"
FROM "nyc-open-data-af2s-4k4p"
