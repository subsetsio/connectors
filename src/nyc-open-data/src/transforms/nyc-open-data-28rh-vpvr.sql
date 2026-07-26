-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "vendor_name",
    "vehicle_typedescription",
    "active_vehicles"
FROM "nyc-open-data-28rh-vpvr"
