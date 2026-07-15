-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "income_size",
    "proportion_of_charities"
FROM "sg-data-d-06b92f48b1aac4d031cfec0bee130c74"
