-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "objectid",
    "meter_number",
    "status",
    "pay_by_cell_number",
    "meter_hours",
    "parking_facility_name",
    "facility",
    "borough",
    "on_street",
    "side_of_street",
    "from_street",
    "to_street",
    "latitude",
    "longitude",
    "x",
    "y",
    "_location" AS location
FROM "nyc-open-data-693u-uax6"
