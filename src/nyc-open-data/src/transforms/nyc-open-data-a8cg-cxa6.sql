-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "status",
    "permit_num",
    strptime("permit_effective_date", '%m/%d/%Y')::DATE AS permit_effective_date,
    strptime("permit_expiration_date", '%m/%d/%Y')::DATE AS permit_expiration_date,
    "plate_state",
    "plate_type",
    "driver_fm_ind",
    "restrict_location",
    "second_plate_state",
    "lost_app_vehicle_stolen",
    "stkr_state",
    strptime("appl_date", '%m/%d/%Y')::DATE AS appl_date,
    "appl_status",
    "appl_definition",
    "city",
    "state",
    "zip",
    "borough"
FROM "nyc-open-data-a8cg-cxa6"
