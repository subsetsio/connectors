-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sensor_name",
    "sensor_id",
    "date_installed",
    "tidally_influenced",
    "date_removed",
    "street_name",
    "borough",
    "zipcode",
    "communityboard",
    "council_district",
    "census_tract_2020",
    "nta",
    "latitude",
    "longitude",
    "sensor_ground_height_above_local_low_point_inches",
    "sensor_location"
FROM "nyc-open-data-kb2e-tjy3"
