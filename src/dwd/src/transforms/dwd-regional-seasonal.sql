-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `period` is a meteorological season ('winter', 'spring', 'summer', 'autumn'). DWD's winter of year Y spans December of Y-1 through February of Y, so a winter row is NOT contained in its own calendar year — the four seasons of a given `year` do not partition that year.
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
FROM "dwd-regional-seasonal"
