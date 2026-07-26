-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "active",
    "vehicle_license_number",
    "_name" AS name,
    "license_type",
    "expiration_date",
    "permit_license_number",
    "dmv_license_plate_number",
    "vehicle_vin_number",
    "wheelchair_accessible",
    "certification_date",
    "hack_up_date",
    "vehicle_year",
    "base_number",
    "base_name",
    "base_type",
    "veh",
    "base_telephone_number",
    "website",
    "base_address",
    "reason",
    "order_date",
    "last_date_updated",
    "last_time_updated"
FROM "nyc-open-data-8wbx-tsch"
