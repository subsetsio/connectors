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
    strptime("suspension_date", '%m/%d/%Y')::DATE AS suspension_date,
    "suspension_reason",
    strptime("last_date_updated", '%m/%d/%Y')::DATE AS last_date_updated,
    "last_time_updated"
FROM "nyc-open-data-jgtb-hmpg"
