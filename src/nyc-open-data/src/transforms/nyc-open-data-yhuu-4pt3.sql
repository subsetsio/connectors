-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "active",
    "permit_license_number",
    "_name" AS name,
    "expiration_date",
    "vehicle_license_number",
    "dmv_license_plate_number",
    "vehicle_vin_number",
    "vehicle_type",
    "certification_date",
    "hack_up_date",
    "vehicle_year",
    "base_number",
    "base_name",
    "base_telephone_number",
    "base_website",
    "base_address",
    "reason",
    "suspension_date",
    "last_date_updated",
    "last_time_updated"
FROM "nyc-open-data-yhuu-4pt3"
