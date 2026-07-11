-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "feature_id",
    "iata_id",
    "name",
    "wmo_id",
    "msc_id",
    "data_provider",
    "dataset_network",
    "auto_man",
    "province_territory",
    "geometry_type",
    "longitude",
    "latitude"
FROM "environment-and-climate-change-canada-swob-stations"
