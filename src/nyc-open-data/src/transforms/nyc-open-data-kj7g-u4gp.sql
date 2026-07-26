-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "station_name",
    "location_name",
    "country",
    "charge_box_id",
    "connector_id",
    "driver_id",
    "id_tag",
    "connected_time",
    "disconnected_time",
    "charge_duration_min",
    "connected_duration_min",
    "energy_provided_kwh",
    "session_status",
    "invalidity_reason"
FROM "nyc-open-data-kj7g-u4gp"
