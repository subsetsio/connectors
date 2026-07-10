-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `period` is the zero-padded calendar month ('01'..'12'), not a date.
-- caution: The most recent `year` is partial: only the months DWD has already released are present, so a year-level aggregate over the latest year is not comparable to earlier years.
-- caution: `region` mixes three aggregation levels: individual federal states, multi-state combinations (Brandenburg/Berlin, Niedersachsen/Hamburg/Bremen, Thueringen/Sachsen-Anhalt) and the national mean 'Deutschland'. Summing or averaging across `region` double-counts — filter to the level you want first.
-- caution: `value` carries a different unit per `variable` (air_temperature_mean in °C, precipitation in mm, sunshine_duration in hours). Never aggregate across `variable`.
-- caution: The variables do not share a start year: air_temperature_mean and precipitation reach back to 1881, sunshine_duration begins in 1951. A query spanning the earlier period silently covers only the first two.
-- caution: Only three variables are published at this resolution; the 10-variable set exists only in the annual table.
SELECT
    "variable",
    "region",
    "year",
    "period",
    "value"
FROM "dwd-regional-monthly"
