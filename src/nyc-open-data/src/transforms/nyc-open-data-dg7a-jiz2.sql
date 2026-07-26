-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "license_number",
    "_name" AS name,
    "_type" AS type,
    "dmv_plate_number",
    "base_name",
    "base_license_number",
    "base_phone_number",
    "base_address",
    "base_website",
    "last_updated_date",
    "last_updated_time"
FROM "nyc-open-data-dg7a-jiz2"
