-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is the latest nine-day forecast snapshot, not a revision history; each run overwrites the forecast available at collection time.
SELECT
    CAST("update_time" AS TIMESTAMP) AS update_time,
    "general_situation",
    strptime("forecast_date", '%Y-%m-%d')::DATE AS forecast_date,
    "week",
    "forecast_wind",
    "forecast_weather",
    "max_temp_c",
    "min_temp_c",
    "max_rh_pct",
    "min_rh_pct",
    "forecast_icon",
    "psr"
FROM "hong-kong-observatory-nine-day-forecast"
