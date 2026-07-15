-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry1",
    "industry2",
    "industry3",
    "at_least_one",
    "unplanned_timeoff",
    "nonscheduled_teleworking"
FROM "sg-data-d-f63f7c88b854a6749493994daa3a484d"
