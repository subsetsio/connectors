-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("feature_id" AS BIGINT) AS feature_id,
    "iata_id",
    "name_fr",
    "name_en",
    "province_territory",
    "auto_man",
    "icao_id",
    "wmo_id",
    CAST("msc_id" AS BIGINT) AS msc_id,
    "dst_time",
    "std_time",
    "data_provider",
    "data_attribution_notice",
    "geometry_type",
    "longitude",
    "latitude"
FROM "environment-and-climate-change-canada-swob-marine-stations"
