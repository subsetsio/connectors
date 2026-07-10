-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- residual: `period` is dropped — it is the constant 'year' at this resolution.
-- caution: `region` mixes three aggregation levels: individual federal states, multi-state combinations (Brandenburg/Berlin, Niedersachsen/Hamburg/Bremen, Thueringen/Sachsen-Anhalt) and the national mean 'Deutschland'. Summing or averaging across `region` double-counts — filter to the level you want first.
-- caution: Berlin, Hamburg and Bremen have no standalone series; they exist only inside the combination regions.
-- caution: `value` carries a different unit per `variable` (air_temperature_mean in °C, precipitation in mm, sunshine_duration in hours, the *_days variables as counts of days per year). Never aggregate across `variable`.
-- caution: The variables do not share a start year: air_temperature_mean and precipitation reach back to 1881, every other variable begins in 1951. A query spanning the earlier period silently covers only those two.
-- caution: Values are area means over the region's footprint, derived from gridded station interpolation — not the reading of any single station, so they do not join to `dwd-stations`.
SELECT
    "variable",
    "region",
    "year",
    "value"
FROM "dwd-regional-annual"
