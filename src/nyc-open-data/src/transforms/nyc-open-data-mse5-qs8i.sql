-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "oid",
    "public_wifi_system",
    "ssid",
    "provider",
    "opendata_dataset_name",
    "hotspot_location_count",
    "pedestrian_corridor_hotspot_count",
    "published_date"
FROM "nyc-open-data-mse5-qs8i"
