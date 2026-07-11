-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Hourly CAMS air-quality data combines historical reanalysis with a short forward forecast window; use `time` to separate historical observations from forward-looking values.
SELECT
    "name",
    "country",
    "latitude",
    "longitude",
    CAST("time" AS TIMESTAMP) AS time,
    "pm10",
    "pm2_5",
    "ozone"
FROM "open-meteo-air-quality"
