-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are calculated for sampled locations and dates; polar-day and polar-night periods may lack ordinary sunrise or sunset times.
SELECT
    "location",
    "lat",
    "lon",
    "date",
    "body",
    "fetched_at",
    "sunrise_time",
    "sunrise_azimuth",
    "sunrise_elevation",
    "sunrise_visible",
    "sunset_time",
    "sunset_azimuth",
    "sunset_elevation",
    "sunset_visible",
    "solarnoon_time",
    "solarnoon_azimuth",
    "solarnoon_elevation",
    "solarnoon_visible",
    "solarmidnight_time",
    "solarmidnight_azimuth",
    "solarmidnight_elevation",
    "solarmidnight_visible"
FROM "norwegian-meteorological-institute-sunrise"
