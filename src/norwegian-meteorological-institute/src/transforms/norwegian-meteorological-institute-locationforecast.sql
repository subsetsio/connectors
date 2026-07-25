-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Forecast rows are for sampled connector locations and each update cycle; use updated_at when comparing forecast revisions for the same location and valid time.
SELECT
    "location",
    "lat",
    "lon",
    "time",
    "updated_at",
    "fetched_at",
    "air_pressure_at_sea_level",
    "air_temperature",
    "cloud_area_fraction",
    "relative_humidity",
    "wind_from_direction",
    "wind_speed",
    "next_1_hours_symbol_code",
    "next_1_hours_precipitation_amount",
    "next_6_hours_symbol_code",
    "next_6_hours_precipitation_amount",
    "next_12_hours_symbol_code"
FROM "norwegian-meteorological-institute-locationforecast"
