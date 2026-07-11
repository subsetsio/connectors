-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an hourly prediction grid; combine year, month, day, and hour before doing time-window analysis.
SELECT
    "station",
    "year",
    "month",
    "day",
    "hour",
    CAST("height_m" AS DOUBLE) AS height_m
FROM "hong-kong-observatory-astronomical-tides-hourly"
