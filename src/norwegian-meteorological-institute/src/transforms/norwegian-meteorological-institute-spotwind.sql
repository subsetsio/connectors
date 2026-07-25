-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows describe aviation spot wind forecasts by named region and flight level; aggregate only after selecting the intended flight_level.
SELECT
    "observation",
    "valid_time",
    "location",
    "flight_level",
    "wind_direction",
    "wind_speed",
    "temperature",
    "fetched_at"
FROM "norwegian-meteorological-institute-spotwind"
