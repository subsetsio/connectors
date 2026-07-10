-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "actual_mean_temp",
    "actual_min_temp",
    "actual_max_temp",
    "average_min_temp",
    "average_max_temp",
    "record_min_temp",
    "record_max_temp",
    "record_min_temp_year",
    "record_max_temp_year",
    "actual_precipitation",
    "average_precipitation",
    "record_precipitation"
FROM "fivethirtyeight-us-weather-history-kjax"
