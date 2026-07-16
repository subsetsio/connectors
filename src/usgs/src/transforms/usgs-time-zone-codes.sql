-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "time_zone_name",
    "time_zone_description",
    "time_zone_utc_offset",
    "time_zone_daylight_savings_time_code",
    "time_zone_daylight_savings_time_name",
    "time_zone_daylight_savings_utc_offset",
    "_lon" AS lon,
    "_lat" AS lat
FROM "usgs-time-zone-codes"
