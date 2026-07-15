-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry1",
    "industry2",
    "at_least_one",
    "unplanned_timeoff",
    "nonscheduled_teleworking"
FROM "sg-data-d-a3e4a9a986e2d5a3713aaec1bfa3648c"
