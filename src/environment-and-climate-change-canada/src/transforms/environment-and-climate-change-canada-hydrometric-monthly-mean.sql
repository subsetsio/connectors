-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "feature_id",
    "IDENTIFIER" AS identifier,
    "STATION_NAME" AS station_name,
    "STATION_NUMBER" AS station_number,
    "PROV_TERR_STATE_LOC" AS prov_terr_state_loc,
    strptime("DATE", '%Y-%m')::DATE AS date,
    "MONTHLY_MEAN_LEVEL" AS monthly_mean_level,
    "MONTHLY_MEAN_DISCHARGE" AS monthly_mean_discharge,
    "geometry_type",
    "longitude",
    "latitude"
FROM "environment-and-climate-change-canada-hydrometric-monthly-mean"
