-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "account_name",
    "active",
    "vehicle_information_complete",
    "bic_number",
    "bic_plate_number",
    "vehicle_body_type",
    "vehicle_make",
    "vehicle_model",
    "vehicle_year",
    "vehicle_engine_make",
    "vehicle_engine_horsepower",
    "vehicle_fuel_type",
    "vehicle_gross_vehicle_weight",
    "vehicle_gross_vehicle_weight_rating_gvwr",
    "vehicle_has_side_guard",
    "vehicle_ownership_type",
    "vehicle_annual_miles_traveled_in_last_year",
    "export_date"
FROM "nyc-open-data-n84m-kx4j"
