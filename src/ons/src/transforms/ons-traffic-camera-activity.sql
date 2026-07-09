-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "value",
    "data_marking",
    CAST("calendar_years" AS BIGINT) AS calendar_years,
    CAST("time" AS BIGINT) AS time,
    "uk_only",
    "geography",
    "dd_mm",
    "daymonth",
    "traffic_camera_area",
    "trafficcameraarea",
    "pedestrians_and_vehicles",
    "pedestriansandvehicles",
    "seasonal_adjustment",
    "seasonaladjustment"
FROM "ons-traffic-camera-activity"
