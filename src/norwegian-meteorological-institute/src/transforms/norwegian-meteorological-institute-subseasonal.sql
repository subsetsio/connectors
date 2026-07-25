-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Subseasonal rows are for sampled connector locations and each model update cycle; use updated_at when comparing forecast revisions for the same location and valid time.
SELECT
    "location",
    "lat",
    "lon",
    "time",
    "updated_at",
    "fetched_at",
    "next_24_hours_air_temperature_max",
    "next_24_hours_air_temperature_max_percentile_10",
    "next_24_hours_air_temperature_max_percentile_90",
    "next_24_hours_air_temperature_mean",
    "next_24_hours_air_temperature_mean_percentile_10",
    "next_24_hours_air_temperature_mean_percentile_90",
    "next_24_hours_air_temperature_min",
    "next_24_hours_air_temperature_min_percentile_10",
    "next_24_hours_air_temperature_min_percentile_90",
    "next_24_hours_precipitation_amount",
    "next_24_hours_precipitation_amount_percentile_10",
    "next_24_hours_precipitation_amount_percentile_90",
    "next_24_hours_probability_of_frost",
    "next_24_hours_probability_of_heavy_precipitation",
    "next_24_hours_probability_of_precipitation"
FROM "norwegian-meteorological-institute-subseasonal"
