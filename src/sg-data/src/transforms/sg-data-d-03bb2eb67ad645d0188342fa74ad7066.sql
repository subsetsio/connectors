-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "date",
    "station",
    "daily_rainfall_total",
    "highest_30_min_rainfall",
    "highest_60_min_rainfall",
    "highest_120_min_rainfall",
    "mean_temperature",
    "maximum_temperature",
    "minimum_temperature",
    "mean_wind_speed",
    "max_wind_speed"
FROM "sg-data-d-03bb2eb67ad645d0188342fa74ad7066"
