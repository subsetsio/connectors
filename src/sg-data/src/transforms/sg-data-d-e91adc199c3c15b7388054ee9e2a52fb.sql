-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age1",
    "reentry_rate_12mth"
FROM "sg-data-d-e91adc199c3c15b7388054ee9e2a52fb"
