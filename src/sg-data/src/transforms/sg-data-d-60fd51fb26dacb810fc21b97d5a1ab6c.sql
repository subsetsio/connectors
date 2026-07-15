-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex1",
    "reentry_rate_12mth"
FROM "sg-data-d-60fd51fb26dacb810fc21b97d5a1ab6c"
