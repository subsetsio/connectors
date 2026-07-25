-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Nowcast rows are for sampled connector locations and each update cycle; use updated_at when comparing forecast revisions for the same location and valid time.
SELECT
    "location",
    "lat",
    "lon",
    "time",
    "updated_at",
    "fetched_at",
    "air_temperature",
    "precipitation_rate",
    "relative_humidity",
    "ultraviolet_index_clear_sky",
    "wind_from_direction",
    "wind_speed",
    "wind_speed_of_gust",
    "next_1_hours_symbol_code",
    "next_1_hours_precipitation_amount"
FROM "norwegian-meteorological-institute-nowcast"
