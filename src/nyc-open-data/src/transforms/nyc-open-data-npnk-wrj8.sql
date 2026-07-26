-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "oid",
    "hotspot_dataset_object_id",
    "public_space_open_space_name",
    "public_space_open_space_proximity",
    "borough_name",
    "neighborhood_tabulation_area_code_nta_code",
    "neighborhood_tabulation_area_name_nta_name",
    "number_of_access_points_per_public_space_open_space",
    "provider",
    "ssid",
    "latitude",
    "longitude",
    "published_date"
FROM "nyc-open-data-npnk-wrj8"
