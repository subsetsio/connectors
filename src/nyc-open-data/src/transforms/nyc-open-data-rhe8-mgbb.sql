-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "license_number",
    "_name" AS name,
    "expiration_date",
    "current_status",
    "dmv_license_plate_number",
    "vehicle_vin_number",
    "vehicle_type",
    "model_year",
    "medallion_type",
    "agent_number",
    "agent_name",
    "agent_telephone_number",
    "agent_website_address",
    "agent_address",
    "last_date_updated",
    "last_time_updated"
FROM "nyc-open-data-rhe8-mgbb"
