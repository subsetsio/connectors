-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sensor_name",
    "sensor_id",
    "flood_start_datetime_gmt",
    "flood_end_datetime_gmt",
    "maximum_flood_depth_inches",
    "time_to_maximum_flood_depth_minutes",
    "time_to_drain_from_peak_minutes",
    "total_duration_minutes",
    "duration_of_flooding_greater_than_4_inches_minutes",
    "duration_of_flooding_greater_than_12_inches_minutes",
    "duration_of_flooding_greater_than_24_inches_minutes",
    "time_series_depth_values_inches",
    "time_series_depth_timestamps_seconds"
FROM "nyc-open-data-aq7i-eu5q"
