-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The `measure` column separates mean, maximum, and minimum daily air temperature; filter it before aggregating values.
SELECT
    "station",
    "measure",
    "year",
    "month",
    "day",
    "value",
    "completeness"
FROM "hong-kong-observatory-daily-temperature"
