-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_year",
    "route_number",
    "service_type",
    "vehicle_typedescription",
    "route_start_date",
    "vendor_code",
    "vendor_name",
    "vendor_affiliation",
    "garage__street_address" AS garage_street_address,
    "garage_city",
    "garage_state",
    "garage_zip",
    "xcoordinates",
    "ycoordinates"
FROM "nyc-open-data-8yac-vygm"
