-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "feature_id",
    "eccc_administrative-zone" AS eccc_administrative_zone,
    "eccc_administrative-zone_name_en" AS eccc_administrative_zone_name_en,
    "eccc_administrative-zone_name_fr" AS eccc_administrative_zone_name_fr,
    "location_name_en",
    "location_name_fr",
    "location_id",
    "url_msc-datamart_observation" AS url_msc_datamart_observation,
    "url_msc-datamart_forecast" AS url_msc_datamart_forecast,
    "geometry_type",
    "longitude",
    "latitude",
    "station"
FROM "environment-and-climate-change-canada-aqhi-stations"
