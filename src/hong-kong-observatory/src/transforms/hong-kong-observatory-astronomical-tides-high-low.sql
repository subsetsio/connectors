-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Predicted tide events are ordinal within each station-day; use `event` with the time and height fields rather than assuming a fixed number of high/low events per day.
SELECT
    "station",
    "year",
    "month",
    "day",
    "event",
    "time",
    CAST("height_m" AS DOUBLE) AS height_m
FROM "hong-kong-observatory-astronomical-tides-high-low"
