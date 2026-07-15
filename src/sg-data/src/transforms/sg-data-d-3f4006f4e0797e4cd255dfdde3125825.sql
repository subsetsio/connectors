-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age1",
    "reentry_rate_6mth"
FROM "sg-data-d-3f4006f4e0797e4cd255dfdde3125825"
