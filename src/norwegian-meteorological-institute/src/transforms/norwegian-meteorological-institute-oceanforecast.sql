-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Ocean forecast rows are for sampled coastal locations and each update cycle; use updated_at when comparing forecast revisions for the same location and valid time.
SELECT
    "location",
    "lat",
    "lon",
    "time",
    "updated_at",
    "fetched_at",
    "sea_surface_wave_from_direction",
    "sea_surface_wave_height",
    "sea_water_speed",
    "sea_water_temperature",
    "sea_water_to_direction"
FROM "norwegian-meteorological-institute-oceanforecast"
