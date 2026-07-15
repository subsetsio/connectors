-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "at_least_one",
    "unplanned_timeoff",
    "nonscheduled_teleworking"
FROM "sg-data-d-ed5664ea4e9d03c7d82810f45c555258"
