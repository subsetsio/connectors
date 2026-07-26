-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "borough",
    "direction",
    "main_street",
    "cross_street",
    "_type" AS type,
    "truck_route",
    "struck_overpass",
    "state_of_operators_license",
    "bridge_identification_number",
    "latitude",
    "longitude"
FROM "nyc-open-data-jdn9-td9w"
